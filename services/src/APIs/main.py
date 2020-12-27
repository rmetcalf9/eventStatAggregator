from .APImain import registerAPI as main_registerAPI

def registerAPIs(appObj):
  nsMain = appObj.flastRestPlusAPIObject.namespace('public/main', description='Main API')
  main_registerAPI(appObj=appObj, APInamespace=nsMain)

