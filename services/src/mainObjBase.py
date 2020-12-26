from baseapp_for_restapi_backend_with_swagger import readFromEnviroment
from object_store_abstraction import createObjectStoreInstance
from SQLAlchemy import SQLAlchemyConnectionFactory
import json
import constants

# This file hosts shared configuration for the main objects
InvalidObjectStoreConfigInvalidJSONException = constants.customExceptionClass('APIAPP_OBJECTSTORECONFIG value is not valid JSON')

class mainObjBaseClass():
  objectStore = None
  APIAPP_OBJECTSTOREDETAILLOGGING = None

  def mainObjBaseClass_init(self, env):

    objectStoreConfigJSON = readFromEnviroment(env, 'APIAPP_OBJECTSTORECONFIG', '{}', None)
    objectStoreConfigDict = None
    try:
      if objectStoreConfigJSON != '{}':
        objectStoreConfigDict = json.loads(objectStoreConfigJSON)
    except Exception as err:
      print(err) # for the repr
      print(str(err)) # for just the message
      print(err.args) # the arguments that the exception has been called with.
      raise(InvalidObjectStoreConfigInvalidJSONException)

    self.APIAPP_OBJECTSTOREDETAILLOGGING = readFromEnviroment(
      env=env,
      envVarName='APIAPP_OBJECTSTOREDETAILLOGGING',
      defaultValue='N',
      acceptableValues=['Y', 'N'],
      nullValueAllowed=True
    ).strip()
    if (self.APIAPP_OBJECTSTOREDETAILLOGGING=='Y'):
      print("APIAPP_OBJECTSTOREDETAILLOGGING set to Y - statement logging enabled")

    fns = {
      'getCurDateTime': self.getCurDateTime
    }

    self.objectStore = SQLAlchemyConnectionFactory(
      objectStoreConfigDict,
      fns,
      detailLogging=(self.APIAPP_OBJECTSTOREDETAILLOGGING=='Y')
    )

  def mainObjBaseClass_exit_gracefully(self):
    self.mqClient.close(wait=True)

