import TestHelperSuperClass
from msgprocObj import msgprocObj
from unittest.mock import MagicMock, call



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
    calls.append(call('Received ' + constants.destinationinboundConnectorScheduleChange + " unrecognised message (not json)"))
    calls.append(call('Complete ' + constants.destinationinboundConnectorScheduleChange))
    TestHelperSuperClass.AssertMagicMockCalls(self, printMock, calls)
