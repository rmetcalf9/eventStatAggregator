

class MissingTransactionContextException(Exception):
  pass

class ConnectionContextBase():
  #if object version is set to none object version checking is turned off
  # object version may be a number or a guid depending on store technology
  callsToStartTransaction = None
  def __init__(self):
    self.callsToStartTransaction = 0

  def _INT_startTransaction(self):
    if self.callsToStartTransaction != 0:
      raise Exception("Disabled ability for nexted transactions")
    self.callsToStartTransaction = self.callsToStartTransaction + 1
    return self._startTransaction()
  def _INT_commitTransaction(self):
    if self.callsToStartTransaction == 0:
      raise Exception("Trying to commit transaction but none started")
    self.callsToStartTransaction = self.callsToStartTransaction - 1
    return self._commitTransaction()
  def _INT_rollbackTransaction(self):
    if self.callsToStartTransaction == 0:
      raise Exception("Trying to rollback transaction but none started")
    self.callsToStartTransaction = self.callsToStartTransaction - 1
    return self._rollbackTransaction()

  def _INT_varifyWeCanMutateData(self):
    if self.callsToStartTransaction == 0:
      raise UnallowedMutationException


  def executeInsideTransaction(self, fnToExecute):
    retVal = None
    self._INT_startTransaction()
    try:
      retVal = fnToExecute(self)
      self._INT_commitTransaction()
    except:
      self._INT_rollbackTransaction()
      raise
    return retVal


class ConnectionContext(ConnectionContextBase):
  mainFactory = None
  connection = None
  transaction = None

  def __init__(self, mainFactory):
    self.mainFactory = mainFactory
    super(ConnectionContext, self).__init__()
    self.connection = self.mainFactory.engine.connect()

  def _startTransaction(self):
    if self.transaction is not None:
      raise Exception("ERROR Starting transaction when there is already one in progress")
    self.transaction = self.connection.begin()

  #Internal function for executing a statement
  ## only called from this file
  def _INT_execute(self, statement):
    if self.transaction is None:
      raise MissingTransactionContextException
    return self.connection.execute(statement.execution_options(autocommit=False))

  def _commitTransaction(self):
    res = self.transaction.commit()
    self.transaction = None
    return res
  def _rollbackTransaction(self):
    res = self.transaction.rollback()
    self.transaction = None
    return res

  def _close(self):
    self.connection.close()
