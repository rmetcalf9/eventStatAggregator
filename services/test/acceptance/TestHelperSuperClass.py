import unittest
import pytz
import datetime
from appObj import appObj
import json
import constants
from unittest.mock import patch
import copy
import uuid
from SessionMock import SessionMock
import TestingHelper

import logging

from nose.plugins.attrib import attr
def wipd(f):
    return attr('wip')(f)

import python_Testing_Utilities


httpOrigin = 'http://a.com'

infoAPIPrefix = '/api/public/info'
mainAPIPrefix = '/api/private/main'

env = {
  'APIAPP_MODE': 'DOCKER',
  'APIAPP_VERSION': 'TEST-3.3.3',
  'APIAPP_FRONTEND': '_',
  'APIAPP_APIURL': 'http://apiurlxxx',
  'APIAPP_FRONTENDURL': 'http://frontenddummytestxxx',
  'APIAPP_APIACCESSSECURITY': '[]',
  'APIAPP_COMMON_ACCESSCONTROLALLOWORIGIN': httpOrigin + ', https://sillysite.com',
  'APIAPP_MQCLIENTCONFIG': '{ \"Type\": \"Memory\" }',
  'APIAPP_OBJECTSTORECONFIG': TestingHelper.Constants.memoryStoreConfigString
}


def getSampleNodeDict(num, type, idprefix="T"):
  return {"props": [
    {"name": "id", "value": idprefix + "-" + str(num).zfill(3)},
    {"name": "text", "value": "Test node " + str(num).zfill(3)},
    {"name": "typeID", "value": type}]
  }

class testClassWithTestClient(unittest.TestCase):
  testClient = None
  standardStartupTime = pytz.timezone('Europe/London').localize(datetime.datetime(2018,1,1,13,46,0,0))

  def _getEnvironment(self):
    raise Exception("Should be overridden")

  def setUp(self):
    self.pre_setUpHook()
    appObj.init(self._getEnvironment(), self.standardStartupTime, testingMode=True)
    self.testClient = appObj.flaskAppObject.test_client()
    self.testClient.testing = True

  def tearDown(self):
    self.testClient = None

  def pre_setUpHook(self):
    pass


ownerUserID = '3efv'
securityEndpointCredentials = {
  "userID": 'admin',
  "roles": [ constants.DefaultHasAccountRole, constants.SecurityEndpointAccessRole ]
}
normalUser1ID = 'reg3rf'
normalUser2ID = 'reg3gf'

class testClassWithHelpers(testClassWithTestClient):

  # acceptedResultList can be none then never assert
  def assertAPIResult(self, methodFN, url, session, data):
    headers = None
    if session != None:
      headers = {
        constants.jwtHeaderName: SessionMock.from_Session(session).getJWTToken()
      }
    if methodFN.__name__ == 'get':
      if data != None:
        raise Exception("Trying to send post data to a get request")
    result = methodFN(
      url,
      headers=headers,
      data=json.dumps(data),
      content_type='application/json'
    )
    return result

  def assertInfoAPIResult(self, methodFN, url, session, data):
    return self.assertAPIResult(methodFN, infoAPIPrefix + url, session, data)
  def assertMainAPIResult(self, methodFN, url, session, data):
    return self.assertAPIResult(methodFN, mainAPIPrefix + url, session, data)

  def assertStatsResultsMatch(self, expected, got):
    self.assertTrue("daily") in got
    self.assertEqual(len(got["daily"]), len(expected["daily"]))
    for c in range(0,len(expected["daily"])):
      python_Testing_Utilities.assertObjectsEqual(
        unittestTestCaseClass=self,
        first=got["daily"][c],
        second=expected["daily"][c],
        msg="Returned stats wrong for day " + expected["daily"][c]["date"],
        ignoredRootKeys=[]
      )
    python_Testing_Utilities.assertObjectsEqual(
      unittestTestCaseClass=self,
      first=got,
      second=expected,
      msg="Wrong main values",
      ignoredRootKeys=["daily"]
    )