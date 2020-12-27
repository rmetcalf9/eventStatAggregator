import datetime
import pytz
from DayWithStats import DayWithStats
import Command
import mq_client_abstraction
import os
import json
from ApiClient import ApiClient
import time

baseURL = "http://0.0.0.0:8097"

queues = [
  {"name": "/queue/eventCountTestQueue001", "tenant": "dev"},
  {"name": "/queue/eventCountTestQueue002", "tenant": "dev"},
  {"name": "/queue/eventCountTestQueue003", "tenant": "dev2"},
  {"name": "/queue/eventCountTestQueue004", "tenant": "dev2"}
]

numDaysToUse = 50
days = {}
curDate =  datetime.datetime.now(pytz.timezone("UTC")) - datetime.timedelta(days = numDaysToUse)
for c in range(0,numDaysToUse):
  dayObj = DayWithStats(curDate)
  days[dayObj.getKey()] = dayObj
  curDate = curDate + datetime.timedelta(days=1)


print("Start of dev machine tester")

mqClient = mq_client_abstraction.createMQClientInstance(configDict=json.loads(os.environ["APIAPP_MQCLIENTCONFIG"]))

commandManager = Command.commandManager()

uniqueTenants = {}
for queue in queues:
  uniqueTenants[queue["tenant"]] = queue["tenant"]
uniqueTenantList = list(uniqueTenants.keys())

apiClient = ApiClient(baseURL)

postBody = {
  "start": days[list(days.keys())[0]].isoformat(),
  "end": days[list(days.keys())[len(days) - 1]].isoformat(),
}

print("Pausing for 2 seconds")
time.sleep(2)

for tenant in uniqueTenants:
  print("Loading inital stats for tenant", tenant)
  results = apiClient.getStatsA(postBody=postBody, name="TestName", tenant=tenant)
  if results is not None:
    for resultDay in results["daily"]:
      dayObj = days[resultDay["date"]]
      dayObj.registerInitialCounts(tenant=tenant, numMessages=resultDay["count"])

context = {
  "running": True,
  "queues": queues,
  "days": days,
  "mqClient": mqClient,
  "apiClient": apiClient,
  "uniqueTenantList": uniqueTenantList
}

while context["running"]:
  commandManager.listCommands()
  command = input("Enter Command:-")
  commandManager.runCommand(command, context)

print("End of dev machine tester")

