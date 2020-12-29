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

  def getStatsB(self, tenant, name, subname, start, end, msg="", checkAndParseResponse=True):
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
      url="/statsB/" + tenant + "/" + name + "/" + subname,
      session=None,
      data=postData
    )
    if not checkAndParseResponse:
      return result
    self.assertEqual(result.status_code, 200, str(msg) + " - " + result.get_data(as_text=True))
    return json.loads(result.get_data(as_text=True))


class test_statsB(helpers):
  def test_zeroStats(self):
    testTime = datetime.datetime.now(pytz.timezone("UTC"))
    #call results as /api/public/info/serverinfo
    result = self.getStatsB(
      tenant=TestingHelper.testingTenant,
      name="SomeName",
      subname="SomeSubname",
      start=testTime,
      end=testTime,
      checkAndParseResponse=True
    )

    expectedRes = {
      "daily": [
        {"daynum": 1, "date": str(testTime.year) + str(testTime.month) + str(testTime.day), "count": 0}
      ]
    }
    self.assertStatsResultsMatch(expected=expectedRes, got=result)


  def test_singleResultOneEvent_onedayrange(self):
    testTime = datetime.datetime.now(pytz.timezone("UTC"))

    appObj.testSendEvent(
      tenant=TestingHelper.testingTenant,
      destination="TESTDESTINATION",
      eventBody=TestingHelper.generateSampleEvent(name="SomeName", subname="SomeSubname", testTime=testTime),
      outputFn=print
    )

    # call results as /api/public/info/serverinfo
    result = self.getStatsB(
      tenant=TestingHelper.testingTenant,
      name="SomeName",
      subname="SomeSubname",
      start=testTime,
      end=testTime,
      checkAndParseResponse=True
    )

    expectedRes = {
      "daily": [
        { "daynum": 1, "date": str(testTime.year) + str(testTime.month) + str(testTime.day), "count": 1}
      ]
    }
    self.assertStatsResultsMatch(expected=expectedRes, got=result)

  def test_singleResultOneEvent_threedayrange(self):
    testTimeDay001 = datetime.datetime.now(pytz.timezone("UTC"))
    testTimeDay002 = testTimeDay001 + datetime.timedelta(days = 1)
    testTimeDay003 = testTimeDay002 + datetime.timedelta(days = 1)

    appObj.testSendEvent(
      tenant=TestingHelper.testingTenant,
      destination="TESTDESTINATION",
      eventBody=TestingHelper.generateSampleEvent(name="SomeName", subname="SomeSubname", testTime=testTimeDay002),
      outputFn=print
    )

    # call results as /api/public/info/serverinfo
    result = self.getStatsB(
      tenant=TestingHelper.testingTenant,
      name="SomeName",
      subname="SomeSubname",
      start=testTimeDay001,
      end=testTimeDay003,
      checkAndParseResponse=True
    )

    expectedRes = {
      "daily": [
        {"daynum": 1, "date": str(testTimeDay001.year) + str(testTimeDay001.month) + str(testTimeDay001.day), "count": 0},
        {"daynum": 2, "date": str(testTimeDay002.year) + str(testTimeDay002.month) + str(testTimeDay002.day), "count": 1},
        {"daynum": 3, "date": str(testTimeDay003.year) + str(testTimeDay003.month) + str(testTimeDay003.day), "count": 0}
      ]
    }
    self.assertStatsResultsMatch(expected=expectedRes, got=result)

  def test_threeResultOneEvent_threedayrange(self):
    testTimeDay001 = datetime.datetime.now(pytz.timezone("UTC"))
    testTimeDay002 = testTimeDay001 + datetime.timedelta(days = 1)
    testTimeDay003 = testTimeDay002 + datetime.timedelta(days = 1)

    appObj.testSendEvent(
      tenant=TestingHelper.testingTenant,
      destination="TESTDESTINATION",
      eventBody=TestingHelper.generateSampleEvent(name="SomeName", subname="SomeSubname", testTime=testTimeDay001),
      outputFn=print
    )
    appObj.testSendEvent(
      tenant=TestingHelper.testingTenant,
      destination="TESTDESTINATION",
      eventBody=TestingHelper.generateSampleEvent(name="SomeName", subname="SomeSubname", testTime=testTimeDay002),
      outputFn=print
    )
    appObj.testSendEvent(
      tenant=TestingHelper.testingTenant,
      destination="TESTDESTINATION",
      eventBody=TestingHelper.generateSampleEvent(name="SomeName", subname="SomeSubname", testTime=testTimeDay003),
      outputFn=print
    )

    # call results as /api/public/info/serverinfo
    result = self.getStatsB(
      tenant=TestingHelper.testingTenant,
      name="SomeName",
      subname="SomeSubname",
      start=testTimeDay001,
      end=testTimeDay003,
      checkAndParseResponse=True
    )

    expectedRes = {
      "daily": [
        {"daynum": 1, "date": str(testTimeDay001.year) + str(testTimeDay001.month) + str(testTimeDay001.day), "count": 1},
        {"daynum": 2, "date": str(testTimeDay002.year) + str(testTimeDay002.month) + str(testTimeDay002.day), "count": 1},
        {"daynum": 3, "date": str(testTimeDay003.year) + str(testTimeDay003.month) + str(testTimeDay003.day), "count": 1}
      ]
    }
    self.assertStatsResultsMatch(expected=expectedRes, got=result)

  def test_differentNumOfEvents_threedayrange(self):
    testTimeDay001 = datetime.datetime.now(pytz.timezone("UTC"))
    testTimeDay002 = testTimeDay001 + datetime.timedelta(days = 1)
    testTimeDay003 = testTimeDay002 + datetime.timedelta(days = 1)

    appObj.testSendEvent(
      tenant=TestingHelper.testingTenant,
      destination="TESTDESTINATION",
      eventBody=TestingHelper.generateSampleEvent(name="SomeName", subname="SomeSubname", testTime=testTimeDay001),
      outputFn=print
    )
    for c in range(0,2):
      appObj.testSendEvent(
        tenant=TestingHelper.testingTenant,
        destination="TESTDESTINATION",
        eventBody=TestingHelper.generateSampleEvent(name="SomeName", subname="SomeSubname", testTime=testTimeDay002),
        outputFn=print
      )
    for c in range(0,3):
      appObj.testSendEvent(
        tenant=TestingHelper.testingTenant,
        destination="TESTDESTINATION",
        eventBody=TestingHelper.generateSampleEvent(name="SomeName", subname="SomeSubname", testTime=testTimeDay003),
        outputFn=print
      )

    # call results as /api/public/info/serverinfo
    result = self.getStatsB(
      tenant=TestingHelper.testingTenant,
      name="SomeName",
      subname="SomeSubname",
      start=testTimeDay001,
      end=testTimeDay003,
      checkAndParseResponse=True
    )

    expectedRes = {
      "daily": [
        {"daynum": 1, "date": str(testTimeDay001.year) + str(testTimeDay001.month) + str(testTimeDay001.day), "count": 1},
        {"daynum": 2, "date": str(testTimeDay002.year) + str(testTimeDay002.month) + str(testTimeDay002.day), "count": 2},
        {"daynum": 3, "date": str(testTimeDay003.year) + str(testTimeDay003.month) + str(testTimeDay003.day), "count": 3}
      ]
    }
    self.assertStatsResultsMatch(expected=expectedRes, got=result)

  def test_differentTenantAndNameAndSubnameIgnored(self):
    testTimeDay001 = datetime.datetime.now(pytz.timezone("UTC"))
    testTimeDay002 = testTimeDay001 + datetime.timedelta(days = 1)
    testTimeDay003 = testTimeDay002 + datetime.timedelta(days = 1)
    testTimeDay004 = testTimeDay003 + datetime.timedelta(days = 1)

    appObj.testSendEvent(
      tenant=TestingHelper.testingTenant,
      destination="TESTDESTINATION",
      eventBody=TestingHelper.generateSampleEvent(name="SomeName", subname="SomeSubname", testTime=testTimeDay001),
      outputFn=print
    )
    for c in range(0,2):
      appObj.testSendEvent(
        tenant=TestingHelper.testingTenant + "2",
        destination="TESTDESTINATION",
        eventBody=TestingHelper.generateSampleEvent(name="SomeName", subname="SomeSubname", testTime=testTimeDay002),
        outputFn=print
      )
    for c in range(0,3):
      appObj.testSendEvent(
        tenant=TestingHelper.testingTenant,
        destination="TESTDESTINATION",
        eventBody=TestingHelper.generateSampleEvent(name="SomeName" + "2", subname="SomeSubname", testTime=testTimeDay003),
        outputFn=print
      )
    for c in range(0,4):
      appObj.testSendEvent(
        tenant=TestingHelper.testingTenant,
        destination="TESTDESTINATION",
        eventBody=TestingHelper.generateSampleEvent(name="SomeName", subname="SomeSubname" + "2", testTime=testTimeDay004),
        outputFn=print
      )

    # call results as /api/public/info/serverinfo
    result = self.getStatsB(
      tenant=TestingHelper.testingTenant,
      name="SomeName",
      subname="SomeSubname",
      start=testTimeDay001,
      end=testTimeDay004,
      checkAndParseResponse=True
    )

    expectedRes = {
      "daily": [
        {"daynum": 1, "date": "{:04d}".format(testTimeDay001.year) + "{:02d}".format(testTimeDay001.month) + "{:02d}".format(testTimeDay001.day), "count": 1},
        {"daynum": 2, "date": "{:04d}".format(testTimeDay002.year) + "{:02d}".format(testTimeDay002.month) + "{:02d}".format(testTimeDay002.day), "count": 0},
        {"daynum": 3, "date": "{:04d}".format(testTimeDay003.year) + "{:02d}".format(testTimeDay003.month) + "{:02d}".format(testTimeDay003.day), "count": 0},
        {"daynum": 4, "date": "{:04d}".format(testTimeDay004.year) + "{:02d}".format(testTimeDay004.month) + "{:02d}".format(testTimeDay004.day), "count": 0}
      ]
    }
    self.assertStatsResultsMatch(expected=expectedRes, got=result)

