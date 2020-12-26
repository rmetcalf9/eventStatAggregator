import json
import uuid
import pytz
import datetime
from dateutil.parser import parse

class EventLogger():
  tz = None
  def __init__(self, timezoneString):
    self.tz = pytz.timezone(timezoneString)
    print("Events logged in timezone:", self.tz)

  def log(self, destination, eventBody, transactionContext, outputFn):
    eventBodyDict = None
    try:
      eventBodyDict = json.loads(eventBody)
    except:
      outputFn("Received(" + destination + ") unrecognised message format (not json)")
      return

    required = ["id", "name", "subname", "timestamp"]

    for curField in required:
      if curField not in eventBodyDict:
        outputFn("Received(" + destination + ") JSON missing " + curField)
        return

    timestampUTC = None
    try:
      dt = parse(eventBodyDict['timestamp'])
      timestampUTC = dt.astimezone(pytz.utc)
    except:
      outputFn("Received(" + destination + ") Invalid timestamp format")
      return


    raise Exception("NI")

