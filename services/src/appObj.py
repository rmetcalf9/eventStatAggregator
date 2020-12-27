#appObj.py - This file contains the main application object
# to be constructed by app.py

#All times will be passed to callers in UTC
# it is up to the callers to convert into any desired user timezone

import pytz

from mainObjBase import mainObjBaseClass

from baseapp_for_restapi_backend_with_swagger import AppObjBaseClass as parAppObj, readFromEnviroment
from flask_restplus import fields
from flask import request
import time
import datetime
import APIs

import constants
import uuid
import json

import logging
import sys

from SQLAlchemy import EventLogger


invalidConfigurationException = constants.customExceptionClass('Invalid Configuration')

class appObjClass(parAppObj, mainObjBaseClass):
  accessControlAllowOriginObj = None

  def setupLogging(self):
    root = logging.getLogger()
    #root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

  def init(self, env, serverStartTime, testingMode = False):
    ##self.setupLogging() Comment in when debugging
    if testingMode:
      pass

    super(appObjClass, self).init(env, serverStartTime, testingMode, serverinfoapiprefix='public/info')

    self.mainObjBaseClass_init(env=env)

  def initOnce(self):
    super(appObjClass, self).initOnce()
    APIs.registerAPIs(self)

    self.flastRestPlusAPIObject.title = "eventStatAggregator`"
    self.flastRestPlusAPIObject.description = "API for eventStatAggregator"

  def stopThread(self):
    ##print("stopThread Called")
    pass

  #override exit gracefully to stop worker thread
  def exit_gracefully(self, signum, frame):
    self.mainObjBaseClass_exit_gracefully()
    self.stopThread()
    super(appObjClass, self).exit_gracefully(signum, frame)

  def testSendEvent(self, tenant, destination, eventBody, outputFn, timezoneString="Europe/London"):
    # function used to inject events directly. Used only for testing in prod events are inserted via msgproc
    eventLogger = EventLogger(timezoneString=timezoneString, getCurDateTimeFn=self.getCurDateTime)
    def fn(transactionContext):
      eventLogger.log(tenant=tenant, destination=destination, eventBody=json.dumps(eventBody), transactionContext=transactionContext, outputFn=outputFn)
    self.objectStore.executeInsideTransaction(fnToExecute=fn)

appObj = appObjClass()
