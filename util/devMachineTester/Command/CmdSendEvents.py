from .Base import Base
import uuid
import json

def getListOfKeyValues(dict):
  retVal = []
  for key in dict.keys():
    retVal.append(dict[key])
  return retVal

def nameGetFn(item):
  return item["name"]

def selectItemsFromList(list, includeAll, subjectText="Queue", itemDisplayFunction=nameGetFn):
  num = 0
  for curItem in list:
    num = num + 1
    print(str(num) + " - " + itemDisplayFunction(curItem))
  if includeAll:
    print("ALL - a")
  retVal = input("Select " + subjectText + " (c to cancel):")
  if retVal == "c":
    return None, True
  if includeAll:
    if retVal == "a":
      return list, False
  try:
    queuNum = int(retVal) - 1
    return [list[queuNum]], False
  except:
    print("invalid")
    return None, True

def selectDay(list, includeAll, minDay=None):
  selMap = {}
  num = 0
  for curDay in list:
    if curDay.isOnOfAfter(minDay):
      num = num + 1
      selMap[num] = curDay
      print(str(num) + " - " + curDay.__str__())
  if includeAll:
    print("ALL - a")
  retVal = input("Select Day (c to cancel):")
  if retVal == "c":
    return None, True
  if includeAll:
    if retVal == "a":
      return list, False
  try:
    queuNum = int(retVal)
    return [selMap[queuNum]], False
  except:
    print("invalid")
    return None, True

class CmdSendEvents(Base):
  def __init__(self):
    super().__init__(name="Send Events", cmd="s")

  def run(self, context):
    selectedQueues, cancel = selectItemsFromList(list=context["queues"], includeAll=True)
    if cancel:
      return
    selectedDay, cancel = selectDay(list=getListOfKeyValues(context["days"]), includeAll=True)
    if cancel:
      return

    for curQueue in selectedQueues:
      for curDay in selectedDay:
        body = {
          "id": str(uuid.uuid4()),
          "name": "TestName",
          "subname": "TestSubname",
          "timestamp": curDay.isoformat()
        }
        print("Sending", json.dumps(body))
        curDay.registerSendMessageTo(destinationQueue=curQueue)
        context["mqClient"].sendStringMessage(destination=curQueue["name"],body=json.dumps(body))
        print("Sent event ", curQueue["name"], " on day ", curDay, body["id"])

