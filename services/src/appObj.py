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

invalidConfigurationException = constants.customExceptionClass('Invalid Configuration')

InvalidObjectStoreConfigInvalidJSONException = constants.customExceptionClass('APIAPP_OBJECTSTORECONFIG value is not valid JSON')
InvalidMqClientConfigInvalidJSONException = constants.customExceptionClass('APIAPP_MQCLIENTCONFIG value is not valid JSON')
InvalidChartUserManagerConfigInvalidJSONException = constants.customExceptionClass('APIAPP_USERMANAGERCONFIG value is not valid JSON')
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

    #This app always needs a JWT key
    if self.APIAPP_JWTSECRET is None:
      print("ERROR - APIAPP_JWTSECRET should always be set")
      raise invalidConfigurationException

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

appObj = appObjClass()
