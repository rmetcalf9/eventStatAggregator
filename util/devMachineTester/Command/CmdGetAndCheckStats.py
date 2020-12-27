from .Base import Base
import uuid
import json
from .CmdSendEvents import selectDay, selectItemsFromList, getListOfKeyValues

class CmdGetAndCheckStats(Base):
  def __init__(self):
    super().__init__(name="Get and Check Stats", cmd="g")

  def run(self, context):
    dayList = getListOfKeyValues(context["days"])
    startDays, cancel = selectDay(list=dayList, includeAll=False)
    if cancel:
      return
    startDay = startDays[0]
    endDays, cancel = selectDay(list=dayList, includeAll=False, minDay=startDay)
    if cancel:
      return
    endDay = endDays[0]

    def itemDisplayFunction(item):
      return item
    tenants, cancel = selectItemsFromList(list=context["uniqueTenantList"], includeAll=True, itemDisplayFunction=itemDisplayFunction)
    if cancel:
      return

    fails = 0
    for tenant in tenants:
      postBody = {
        "start": startDay.isoformat(),
        "end": endDay.isoformat(),
      }
      results = context["apiClient"].getStatsA(postBody=postBody, name="TestName", tenant=tenant)
      if results is None:
        return

      for resultDay in results["daily"]:
        dayObj = context["days"][resultDay["date"]]
        if not dayObj.checkResultsAgainst(resultDay, tenant=tenant):
          fails += 1

    if fails > 0:
      print("There were " + str(fails) + " days with mismatches")

    if fails == 0:
      print("No failures!!!")

