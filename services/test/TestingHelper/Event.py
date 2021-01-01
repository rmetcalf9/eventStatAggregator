import datetime
import pytz
import uuid

def generateSampleEvent(name="TestName001",subname="TestSubName001", testTime=datetime.datetime.now(pytz.timezone("UTC"))):
  return {
    "id": str(uuid.uuid4()),
    "name": name,
    "subname": subname,
    "timestamp": testTime.isoformat()
  }

def getSampleStatResponse(name, daily, subname=None, startDate=None, endDate=None):
  retVal = {
    "statName": name,
    "statStartDateStr": "{:04d}{:02d}{:02d}".format(startDate.year, startDate.month, startDate.day),
    "statEndDateStr": "{:04d}{:02d}{:02d}".format(endDate.year, endDate.month, endDate.day),
    "daily": daily
  }
  if subname is not None:
    retVal["statSubname"] = subname
  return retVal