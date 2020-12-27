import datetime
import pytz
import uuid

def generateSampleEvent(name="TestName001", testTime=datetime.datetime.now(pytz.timezone("UTC"))):
  return {
    "id": str(uuid.uuid4()),
    "name": name,
    "subname": "TestSubName001",
    "timestamp": testTime.isoformat()
  }

