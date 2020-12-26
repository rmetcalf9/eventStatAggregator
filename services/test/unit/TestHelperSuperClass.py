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
