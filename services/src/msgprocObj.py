import signal
import time
from baseapp_for_restapi_backend_with_swagger import readFromEnviroment
import datetime
import pytz
from mainObjBase import mainObjBaseClass
import constants
import ConnectorTypes
import Store
import threading
#import MessageProcessors
#from IncommingConnectionScheduleManager import IncommingConnectionsScheduleManagerClass

class ThreadSafeMessageToProcess():
  lock=None
  inProgress=None
  destination=None
  body=None

  def __init__(self):
    self.lock = threading.Lock()
    self.inProgress = False
    self.destination = None
    self.body = None

  def setMessageToProcess(self, destination, body):
    self.lock.acquire(blocking=True, timeout=-1)
    if self.inProgress:
      raise Exception("ERROR MESSAGE already in progress can't set")
    if self.body is not None:
      raise Exception("ERROR MESSAGE body not taken can't set")
    if self.destination is not None:
      raise Exception("ERROR MESSAGE destination not taken can't set")
    self.destination = destination
    self.body = body
    self.lock.release()

  def startProcessing(self):
    self.lock.acquire(blocking=True, timeout=-1)
    if self.inProgress:
      raise Exception("ERROR MESSAGE already in progress can't start")
    if self.body is None:
      self.lock.release()
      return None, None
    if self.destination is None:
      raise Exception("ERROR MESSAGE no destination can't start")
    retVal = (self.body, self.destination)
    self.inProgress = True
    self.lock.release()
    return retVal

  def processingComplete(self):
    self.lock.acquire(blocking=True, timeout=-1)
    if not self.inProgress:
      raise Exception("ERROR MESSAGE NOT in progress can't complete")
    if self.body is None:
      raise Exception("ERROR MESSAGE no body can't complete")
    if self.destination is None:
      raise Exception("ERROR MESSAGE no destination can't complete")
    self.inProgress = False
    self.body = None
    self.destination = None
    self.lock.release()

  def isInProgress(self):
    self.lock.acquire(blocking=True, timeout=-1)
    retVal = self.inProgress
    self.lock.release()
    return retVal


class msgProcObjClass(mainObjBaseClass):
  APIAPP_VERSION = None
  schedular = None

  msgToBeProcessed = None

  class ServerTerminationError(Exception):
    def __init__(self):
      pass
    def __str__(self):
      return "Server Terminate Error"

  isInitOnce = False
  def init(self, env, args):
    self.msgToBeProcessed = ThreadSafeMessageToProcess()
    self.mainObjBaseClass_init(env=env)

    self.APIAPP_VERSION = readFromEnviroment(env, 'APIAPP_VERSION', None, None)

    print("eventStatAggregator -> Message Processor")
    print("APIAPP_VERSION", self.APIAPP_VERSION)

    if (self.isInitOnce):
      return
    self.isInitOnce = True
    self.initOnce()

    if len(args)<2:
      raise Exception("Command line args must include at least one destination to subscribe to")

  def initOnce(self):

    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully) #sigterm is sent by docker stop command

  def exit_gracefully(self, signum, frame):
    print("Exit Gracefully called")
    self.mainObjBaseClass_exit_gracefully()
    raise self.ServerTerminationError()

  def LocalMessageProcessorFunctionCaller(self, destination, body):
    self.msgToBeProcessed.setMessageToProcess(destination=destination, body=body)
    #sleep this thread until the main thread has completed processing
    # this prevents us from taking another message before this one is complete
    # required because scrapy will only run on main thread
    while self.msgToBeProcessed.isInProgress():
      time.sleep(0.5)

  def LocalMessageProcessorFunction_inboundConnectorExecutions(self, destination, body, outputFn=print):
    def dbfn(storeConnection):
      ConnectorTypes.MessageProcessorFunction(
        destination=destination,
        body=body,
        commonAppObj=self,
        outputFn=outputFn,
        connectorLogic=self.connectorLogic,
        storeConnection=storeConnection,
        linkvisAPIClientInstance=self.linkvisAPIClientInstance,
        userManagementAPIClientInstance=self.userManagementAPIClientInstance
      )
    self.objectStore.executeInsideTransaction(dbfn)

  def LocalMessageProcessorFunction_notifyConnectorGraphDeleted(self, destination, body, outputFn=print):
    print("Recieved " + destination + ":" + body + " TODO handle")


  def LocalMessageProcessorFunction(self, destination, body, outputFn=print):
    if destination not in self.destinationsSubscribedTo:
      raise Exception("Not subscribed to " + destination)
    self.destinationsSubscribedTo[destination](msgprocObj=self, destination=destination, body=body, outputFn=outputFn)


  def run(self):
    if (self.isInitOnce == False):
      raise Exception('Trying to run app without initing')

    for x in self.destinationsSubscribedTo:
      print("Subscribing to " + constants.destinationInboundConnector)
      self.mqClient.subscribeToDestination(destination=x,msgRecieveFunction=self.LocalMessageProcessorFunctionCaller)

    try:
      body = None
      while True:
        self.mqClient.processLoopIteration()
        if self.schedular is not None:
          self.schedular.processLoopIteration()
        (body, destination) = self.msgToBeProcessed.startProcessing()
        if body is not None:
          self.LocalMessageProcessorFunction(destination=destination, body=body)
          self.msgToBeProcessed.processingComplete()
        time.sleep(0.1)
        pass
    except self.ServerTerminationError:
      pass

  curDateTimeOverrideForTesting = None
  def setTestingDateTime(self, val):
    self.curDateTimeOverrideForTesting = val
  def getCurDateTime(self):
    if self.curDateTimeOverrideForTesting is None:
      return datetime.datetime.now(pytz.timezone("UTC"))
    return self.curDateTimeOverrideForTesting

msgprocObj = msgProcObjClass()
