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

