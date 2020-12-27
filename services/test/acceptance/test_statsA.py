# simple test to make sure baseapp is properly configured

import TestHelperSuperClass
import python_Testing_Utilities
import json
import TestingHelper
import datetime
import pytz

class helpers(TestHelperSuperClass.testClassWithHelpers):
  def _getEnvironment(self):
    return TestHelperSuperClass.env

  def getStatsA(self, tenant, name, start, end, msg="", checkAndParseResponse=True):
    startUse = start
    endUse = end
    if startUse is None:
      startUse = datetime.datetime.now(pytz.timezone("UTC"))
    if endUse is None:
      endUse = datetime.datetime.now(pytz.timezone("UTC"))
    postData = {
      "start": startUse.isoformat(),
      "end": endUse.isoformat()
    }
    result = self.assertMainAPIResult(
      methodFN=self.testClient.post,
      url="/statsA/" + tenant + "/" + name,
      session=None,
      data=postData
    )
    if not checkAndParseResponse:
      return result
    self.assertEqual(result.status_code, 200, str(msg) + " - " + result.get_data(as_text=True))
    return json.loads(result.get_data(as_text=True))


class test_statsA(helpers):
  def test_zeroStats(self):
    #call results as /api/public/info/serverinfo
    result = self.getStatsA(
      tenant=TestingHelper.testingTenant,
      name="SomeName",
      start=None,
      end=None,
      checkAndParseResponse=True
    )

    expectedRes = {
      'Server': {
        'APIAPP_APIDOCSURL': '_',
        'Version': 'TEST-3.3.3',
        'APIAPP_FRONTENDURL': TestHelperSuperClass.env['APIAPP_FRONTENDURL']
      },
      'Derived': None
    }

    python_Testing_Utilities.assertObjectsEqual(
      unittestTestCaseClass=self,
      first=result,
      second=expectedRes,
      msg="Returned stats wrong",
      ignoredRootKeys=[]
    )