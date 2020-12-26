import TestHelperSuperClass
from msgprocObj import msgprocObj
from unittest.mock import MagicMock, call
import constants
import json
import uuid

def generateSampleEvent():
  return {
    "id": str(uuid.uuid4()),
    "name": "TestName001",
    "subname": "TestSubName001",
    "timestamp": "TODO"
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


  #TODO INvalid timestamp date 31 Feb
