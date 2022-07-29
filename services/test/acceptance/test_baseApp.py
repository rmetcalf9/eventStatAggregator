# simple test to make sure baseapp is properly configured

import TestHelperSuperClassAcceptance
import python_Testing_Utilities
import json

class helpers(TestHelperSuperClassAcceptance.testClassWithHelpers):
  def _getEnvironment(self):
    return TestHelperSuperClassAcceptance.env

class test_adminapi(helpers):
  def test_infoEndpoint(self):
    #call results as /api/public/info/serverinfo
    result = self.assertInfoAPIResult(
      methodFN=self.testClient.get,
      url="/serverinfo",
      session=None,
      data=None
    )
    self.assertEqual(result.status_code, 200, msg="Create user call returned error")
    apiResult = json.loads(result.get_data(as_text=True))

    expectedRes = {
      'Server': {
        'APIAPP_APIDOCSURL': '_',
        'Version': 'TEST-3.3.3',
        'APIAPP_FRONTENDURL': TestHelperSuperClassAcceptance.env['APIAPP_FRONTENDURL']
      },
      'Derived': None
    }

    python_Testing_Utilities.assertObjectsEqual(
      unittestTestCaseClass=self,
      first=apiResult,
      second=expectedRes,
      msg="Server Info return wrong",
      ignoredRootKeys=[]
    )
