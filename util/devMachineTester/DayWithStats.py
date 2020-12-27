

class DayWithStats():
  dt = None
  tenantSendStats = None
  def __init__(self, dt):
    self.dt = dt
    self.tenantSendStats = {}

  def __str__(self):
    return self.dt.__str__()

  def isoformat(self):
    return self.dt.isoformat()

  def _ensureStatValueExists(self, tenant, queueName):
    if tenant not in self.tenantSendStats:
      self.tenantSendStats[tenant] = {}
    if queueName not in self.tenantSendStats[tenant]:
      self.tenantSendStats[tenant][queueName] = 0

  def registerSendMessageTo(self, destinationQueue):
    self._ensureStatValueExists(tenant=destinationQueue["tenant"], queueName=destinationQueue["name"])
    self.tenantSendStats[destinationQueue["tenant"]][destinationQueue["name"]] += 1

  def registerInitialCounts(self, tenant, numMessages):
    self._ensureStatValueExists(tenant=tenant, queueName="Initial")
    self.tenantSendStats[tenant]["Initial"] += numMessages



  def isOnOfAfter(self, day):
    if day is None:
      return True
    return self.dt >= day.dt

  def getKey(self):
    return "{:04d}".format(self.dt.year) + "{:02d}".format(self.dt.month) + "{:02d}".format(self.dt.day)

  def checkResultsAgainst(self, dayResults, tenant):
    if self.getKey() != dayResults["date"]:
      print("FAILED " + self.getKey() + " - wrong key")
      return False
    expected = 0
    if tenant in self.tenantSendStats:
      for queue in self.tenantSendStats[tenant].keys():
        expected += self.tenantSendStats[tenant][queue]
    if expected != dayResults["count"]:
      print("FAILED " + self.getKey() + " - expected " + str(expected) + " got " + str(dayResults["count"]))
      return False
    print("PASSED " + self.getKey() + " - had " + str(dayResults["count"]) + " and it matched!!!")
    return True

