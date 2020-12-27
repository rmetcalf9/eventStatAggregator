import json
import uuid
import pytz
import datetime
from dateutil.parser import parse

class EventLogger():
  tz = None
  getCurDateTimeFn = None
  def __init__(self, timezoneString, getCurDateTimeFn):
    self.tz = pytz.timezone(timezoneString)
    self.getCurDateTimeFn = getCurDateTimeFn
    print("Events logged in timezone:", self.tz)

  def log(self, tenant, destination, eventBody, transactionContext, outputFn):
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

    dtInLocalTimeZone = dt.astimezone(self.tz)

    print("dt=", dtInLocalTimeZone)
    print("dtInLocalTimeZone", dtInLocalTimeZone)

    id = str(uuid.uuid4())
    event_name = eventBodyDict["name"]
    event_subname = eventBodyDict["subname"]
    event_id = eventBodyDict["id"]
    dom = dtInLocalTimeZone.day
    month = dtInLocalTimeZone.month
    year = dtInLocalTimeZone.year
    event_date = dtInLocalTimeZone

    curTime = self.getCurDateTimeFn()
    query = transactionContext.mainFactory.objDataTable.insert().values(
      creation_date=curTime,
      tenant=tenant,
      event_name=event_name,
      event_subname=event_subname,
      event_id=event_id,
      dom=dom,
      month=month,
      year=year,
      event_date=event_date
    )

    result = transactionContext._INT_execute(query)
    if len(result.inserted_primary_key) != 1:
      raise Exception('Event Logger failed - wrong number of rows inserted')

    outputFn("Received(" + destination + ") " + event_name + ":" + event_subname + " OK")
