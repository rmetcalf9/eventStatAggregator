# simple test to make sure baseapp is properly configured

import TestHelperSuperClass
import python_Testing_Utilities
import json
import TestingHelper
import datetime
import pytz
from appObj import appObj


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
      "daily": [
      ]
    }

    python_Testing_Utilities.assertObjectsEqual(
      unittestTestCaseClass=self,
      first=result,
      second=expectedRes,
      msg="Returned stats wrong",
      ignoredRootKeys=[]
    )

  def test_singleResultOneEvent_onedayrange(self):
    testTime = datetime.datetime.now(pytz.timezone("UTC"))

    appObj.testSendEvent(
      tenant=TestingHelper.testingTenant,
      destination="TESTDESTINATION",
      eventBody=TestingHelper.generateSampleEvent(name="SomeName", testTime=testTime),
      outputFn=print
    )

    # call results as /api/public/info/serverinfo
    result = self.getStatsA(
      tenant=TestingHelper.testingTenant,
      name="SomeName",
      start=testTime,
      end=testTime,
      checkAndParseResponse=True
    )

    expectedRes = {
      "daily": [
        { "daynum": 1, "date": str(testTime.year) + str(testTime.month) + str(testTime.day), "count": 1}
      ]
    }

    print("X", result)

    self.assertTrue("daily") in result
    self.assertEqual(len(result["daily"]), 1)
    python_Testing_Utilities.assertObjectsEqual(
      unittestTestCaseClass=self,
      first=result["daily"][0],
      second=expectedRes["daily"][0],
      msg="Returned stats wrong",
      ignoredRootKeys=[]
    )

    #TODO Single result bigger range with 0's on day before and after

    #TODO Date param test (results before and after) (one event per day)

    #TODO 5 events on single day


