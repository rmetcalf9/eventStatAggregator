import TestHelperSuperClass
from msgprocObj import msgprocObj
from unittest.mock import MagicMock, call
import constants
import json
import uuid
import datetime
import pytz
from sqlalchemy import and_
import TestingHelper


def generateSampleEvent(testTime=datetime.datetime.now(pytz.timezone("UTC"))):
  return {
    "id": str(uuid.uuid4()),
    "name": "TestName001",
    "subname": "TestSubName001",
    "timestamp": testTime.isoformat()
  }

class helpers(TestHelperSuperClass.msgProcTestBaseClass):
  pass

#@TestHelperSuperClass.wipd
class test_proc_notifyConnector_GraphDeleted(helpers):

  def test_invalidMessageNotJSON(self):
    printMock = MagicMock()
    msgprocObj.LocalMessageProcessorFunction(
      destination=TestHelperSuperClass.testQueue001,
      body="DataThatISNotJSON",
      outputFn=printMock
    )
    calls = []
    calls.append(call('Received(/queue/testQueue) unrecognised message format (not json)'))
    TestHelperSuperClass.AssertMagicMockCalls(self, printMock, calls)

  def test_invalidMessageMissingRequired(self):
    printMock = MagicMock()
    msgprocObj.LocalMessageProcessorFunction(
      destination=TestHelperSuperClass.testQueue001,
      body="{}",
      outputFn=printMock
    )
    calls = []
    calls.append(call('Received(/queue/testQueue) JSON missing id'))
    TestHelperSuperClass.AssertMagicMockCalls(self, printMock, calls)

  def test_invalidTimestampFormat(self):
    sampleEvent = generateSampleEvent()
    sampleEvent["timestamp"] = "INVALIDTIMESTAMP"
    printMock = MagicMock()
    msgprocObj.LocalMessageProcessorFunction(
      destination=TestHelperSuperClass.testQueue001,
      body=json.dumps(sampleEvent),
      outputFn=printMock
    )
    calls = []
    calls.append(call('Received(/queue/testQueue) Invalid timestamp format'))
    TestHelperSuperClass.AssertMagicMockCalls(self, printMock, calls)

  def test_invalidTimestampFormat(self):
    sampleEvent = generateSampleEvent()
    sampleEvent["timestamp"] = "INVALIDTIMESTAMP"
    printMock = MagicMock()
    msgprocObj.LocalMessageProcessorFunction(
      destination=TestHelperSuperClass.testQueue001,
      body=json.dumps(sampleEvent),
      outputFn=printMock
    )
    calls = []
    calls.append(call('Received(/queue/testQueue) Invalid timestamp format'))
    TestHelperSuperClass.AssertMagicMockCalls(self, printMock, calls)

  def test_invalidTimestamp31Feb(self):
    sampleEvent = generateSampleEvent()
    sampleEvent["timestamp"] = "2020-02-31T15:23:30.965819+00:00"
    printMock = MagicMock()
    msgprocObj.LocalMessageProcessorFunction(
      destination=TestHelperSuperClass.testQueue001,
      body=json.dumps(sampleEvent),
      outputFn=printMock
    )
    calls = []
    calls.append(call('Received(/queue/testQueue) Invalid timestamp format'))
    TestHelperSuperClass.AssertMagicMockCalls(self, printMock, calls)

  def test_invalidTimestamp31Feb(self):
    sampleEvent = generateSampleEvent()
    sampleEvent["timestamp"] = "2020-02-31T15:23:30.965819+00:00"
    printMock = MagicMock()
    msgprocObj.LocalMessageProcessorFunction(
      destination=TestHelperSuperClass.testQueue001,
      body=json.dumps(sampleEvent),
      outputFn=printMock
    )
    calls = []
    calls.append(call('Received(/queue/testQueue) Invalid timestamp format'))
    TestHelperSuperClass.AssertMagicMockCalls(self, printMock, calls)

  def test_valid(self):
    testTime = datetime.datetime.now(pytz.timezone("UTC"))
    msgprocObj.setTestingDateTime(testTime)
    sampleEvent = generateSampleEvent(testTime=testTime)
    sampleEvent["timestamp"] = "2020-09-29T15:23:30.965819+05:00"

    printMock = MagicMock()
    msgprocObj.LocalMessageProcessorFunction(
      destination=TestHelperSuperClass.testQueue001,
      body=json.dumps(sampleEvent),
      outputFn=printMock
    )
    calls = []
    calls.append(call("Received(/queue/testQueue) " + sampleEvent["name"] + ":" + sampleEvent["subname"] + " OK"))
    TestHelperSuperClass.AssertMagicMockCalls(self, printMock, calls)


    def fn(queryContext):
      query = queryContext.mainFactory.objDataTable.select(whereclause=(
        and_(
          queryContext.mainFactory.objDataTable.c.tenant == TestingHelper.testingTenant,
          queryContext.mainFactory.objDataTable.c.event_name == sampleEvent["name"],
          queryContext.mainFactory.objDataTable.c.event_subname == sampleEvent["subname"],
          queryContext.mainFactory.objDataTable.c.event_id == sampleEvent["id"]
        )
      ))
      result = queryContext._INT_executeQuery(query)
      rowsReturned = 0
      for row in result:
        rowsReturned += 1
        print(row)
        #self.assertEqual(row[0], 1) ID in table
        ##self.assertEqual(row[1],testTime) #
        self.assertEqual(row[2],TestingHelper.testingTenant)
        self.assertEqual(row[3],sampleEvent["name"])
        self.assertEqual(row[4],sampleEvent["subname"])
        self.assertEqual(row[5],sampleEvent["id"]) # event_id
        self.assertEqual(row[6],29) #day of month
        self.assertEqual(row[7],9) # mon
        self.assertEqual(row[8],2020) # year
        ##self.assertEqual(row[8],testTime) # event timestamp (TZ info not included in result)
      self.assertEqual(rowsReturned, 1)

    msgprocObj.objectStore.executeInsideConnectionContext(fn)

