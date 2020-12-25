import signal
import time
from baseapp_for_restapi_backend_with_swagger import readFromEnviroment
import datetime
import pytz
from mainObjBase import mainObjBaseClass
import constants
import threading
import json
import mq_client_abstraction

#import MessageProcessors
#from IncommingConnectionScheduleManager import IncommingConnectionsScheduleManagerClass

InvalidMqClientConfigInvalidJSONException = constants.customExceptionClass('APIAPP_MQCLIENTCONFIG value is not valid JSON')
InvalidListenDestListException = constants.customExceptionClass('APIAPP_LISTENDESTLIST value is not valid JSON')


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
  mqClient = None

  msgToBeProcessed = None
  destinationsSubscribedTo = None #Subscriptions this instance should make (read form args)

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

    mqClientConfigJSON = readFromEnviroment(env, 'APIAPP_MQCLIENTCONFIG', '{}', None)
    mqClientConfigDict = None
    try:
      if mqClientConfigJSON != '{}':
        mqClientConfigDict = json.loads(mqClientConfigJSON)
    except Exception as err:
      print(err) # for the repr
      print(str(err)) # for just the message
      print(err.args) # the arguments that the exception has been called with.
      raise(InvalidMqClientConfigInvalidJSONException)

    self.mqClient = mq_client_abstraction.createMQClientInstance(configDict=mqClientConfigDict)

    listenGuestListJSON = readFromEnviroment(env, 'APIAPP_LISTENDESTLIST', '[]', None)
    listenGuestList = None
    try:
      if listenGuestListJSON != '[]':
        listenGuestList = json.loads(listenGuestListJSON)
    except Exception as err:
      print(err) # for the repr
      print(str(err)) # for just the message
      print(err.args) # the arguments that the exception has been called with.
      raise(InvalidListenDestListException)

    if listenGuestList is None:
      raise Exception("Must set environemnt variable APIAPP_LISTENDESTLIST")

    if not isinstance(listenGuestList, list):
      raise Exception("APIAPP_LISTENDESTLIST is not a list")
    if len(listenGuestList) == 0:
      raise Exception("APIAPP_LISTENDESTLIST must have at least one item")


    self.destinationsSubscribedTo = []
    for dest in listenGuestList:
      self.destinationsSubscribedTo.append(dest)


    if (self.isInitOnce):
      return
    self.isInitOnce = True
    self.initOnce()

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

  def LocalMessageProcessorFunction(self, destination, body, outputFn=print):
    if destination not in self.destinationsSubscribedTo:
      # should never reach here
      raise Exception("Not subscribed to " + destination)
    # TODO Wrap message into DB context and run processing
    raise Exception("Not implemented process message")


  def run(self):
    if (self.isInitOnce == False):
      raise Exception('Trying to run app without initing')

    for x in self.destinationsSubscribedTo:
      print("Subscribing to " + x)
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
