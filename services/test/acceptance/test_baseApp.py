# simple test to make sure baseapp is properly configured

import TestHelperSuperClass
import python_Testing_Utilities
import json

class helpers(TestHelperSuperClass.testClassWithHelpers):
  def _getEnvironment(self):
    return TestHelperSuperClass.env

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
        'APIAPP_FRONTENDURL': TestHelperSuperClass.env['APIAPP_FRONTENDURL']
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
