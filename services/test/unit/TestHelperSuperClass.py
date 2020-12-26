import unittest
from msgprocObj import msgprocObj
import pytz
import datetime
import TestingHelper

from nose.plugins.attrib import attr
def wipd(f):
  return attr('wip')(f)

testQueue001 = '/queue/testQueue'

env = {
  'APIAPP_VERSION': 'TESTMSGPROC-3.3.3',
  'APIAPP_LISTENDESTLIST': '["' + testQueue001 + '"]',
  'APIAPP_OBJECTSTORECONFIG': TestingHelper.Constants.memoryStoreConfigString
}

class msgProcTestBaseClass(unittest.TestCase):
  standardStartupTime = pytz.timezone('Europe/London').localize(datetime.datetime(2018,1,1,13,46,0,0))

  def _getEnvironment(self):
    return env

  def setUp(self):
    msgprocObj.init(self._getEnvironment(), args=["UnitTests.py (Fake)"])
    msgprocObj.setTestingDateTime(self.standardStartupTime)

  def tearDown(self):
    pass

def AssertMagicMockCalls(testClassInstance, mockObj, calls):
  mockObj.assert_has_calls(calls, any_order=False)
  if mockObj.call_count > len(calls):
    print("More mock calls then expected in test")
    print("*** Actual Mock Calls were")
    # This code works in first example but dosen't smell right
    #  as there may be mutiple calls.
    print(mockObj.call_args)
  testClassInstance.assertEqual(len(calls), mockObj.call_count, msg="Wrong number of calls")

