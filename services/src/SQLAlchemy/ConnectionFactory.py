from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, BigInteger, DateTime, JSON, func, UniqueConstraint, and_, Text, select
from sqlalchemy.pool import StaticPool

from .ConnectionContext import ConnectionContext

objectStoreHardCodedVersionInteger = 1

class SQLAlchemyConnectionFactory():
  engine = None
  objDataTable = None
  verTable = None
  objectPrefix = None
  def __init__(self, ConfigDict, externalFns, detailLogging):


    if ConfigDict is None:
      raise Exception("Default config not implemented")

    if "Type" not in ConfigDict:
      raise Exception("Type not in store configuration")

    if ConfigDict["Type"] != "SQLAlchemy":
      raise Exception("Type not SQLAlchemy - Uses same format config as objectstore but only implemented in SQLAlchemy")


    if detailLogging:
      logging.basicConfig()
      logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    if "connectionString" not in ConfigDict:
      raise ObjectStoreConfigError("APIAPP_OBJECTSTORECONFIG SQLAlchemy ERROR - Expected connectionString")
    if "objectPrefix" in ConfigDict:
      self.objectPrefix = ConfigDict["objectPrefix"]
    else:
      self.objectPrefix = ""

    connect_args = None
    if "ssl_ca" in ConfigDict:
      #print("ssl_ca:", ConfigDict['ssl_ca'])
      if not os.path.isfile(ConfigDict['ssl_ca']):
        raise Exception("Supplied ssl_ca dosen't exist")
      connect_args = {
        "ssl": {'ca': ConfigDict['ssl_ca']}
      }

    #My experiment for SSL https://code.metcarob.com/node/249
    #debugging https://github.com/PyMySQL/PyMySQL/blob/master/pymysql/connections.py

    otherArgsForCreateEngine = {}
    if "create_engine_args" in ConfigDict:
      otherArgsForCreateEngine = ConfigDict["create_engine_args"]
    else:
      otherArgsForCreateEngine = {
        "pool_recycle": 3600,
        "pool_size": 40,
        "max_overflow": 0
      }
      if ConfigDict["connect_args"] is not None:
        otherArgsForCreateEngine["connect_args"] = ConfigDict["connect_args"]

    if "poolclass" in otherArgsForCreateEngine:
      if otherArgsForCreateEngine["poolclass"] == "StaticPool":
        otherArgsForCreateEngine["poolclass"] = StaticPool

    self.engine = create_engine(ConfigDict["connectionString"], **otherArgsForCreateEngine)


    metadata = MetaData()
    #(objDICT, objectVersion, creationDate, lastUpdateDate)
    #from https://stackoverflow.com/questions/15157227/mysql-varchar-index-length
    #MySQL assumes 3 bytes per utf8 character. 255 characters is the maximum index size you can specify per column, because 256x3=768, which breaks the 767 byte limit.
    self.objDataTable = Table(self.objectPrefix + 'events', metadata,
      Column('id', Integer, primary_key=True),
      Column('creation_date', DateTime(timezone=True)),
      Column('event_name', String(255), index=True),
      Column('event_subname', String(255), index=True),
      Column('event_id', String(255), index=True),
      Column('dom', Integer),
      Column('month', Integer),
      Column('year', Integer),
      Column('event_date', DateTime(timezone=True)),
      UniqueConstraint('id', name=self.objectPrefix + '_objData_ix1')
    )
    self.verTable = Table(self.objectPrefix + '_ver', metadata,
        Column('id', Integer, primary_key=True),
        Column('first_installed_ver', Integer),
        Column('current_installed_ver', Integer),
        Column('creationDate_iso8601', String(length=40)),
        Column('lastUpdateDate_iso8601', String(length=40))
    )
    metadata.create_all(self.engine)

    self._INT_setupOrUpdateVer(externalFns)

  #AppObj passed in as None
  def _INT_setupOrUpdateVer(self, externalFns):
    def someFn(connectionContext):
      curTime = externalFns['getCurDateTime']()
      query = self.verTable.select()
      result = connectionContext._INT_execute(query)
      if result.rowcount != 1:
        if result.rowcount != 0:
          if result.rowcount != -1:
            raise Exception('invalid database structure - can\'t read version - rowcount was ' + str(result.rowcount))
        #There are 0 rows, create one
        query = self.verTable.insert().values(
          first_installed_ver=objectStoreHardCodedVersionInteger,
          current_installed_ver=objectStoreHardCodedVersionInteger,
          creationDate_iso8601=curTime.isoformat(),
          lastUpdateDate_iso8601=curTime.isoformat()
        )
        result = connectionContext._INT_execute(query)
        return
      firstRow = result.first()
      if objectStoreHardCodedVersionInteger == firstRow['current_installed_ver']:
        return
      raise Exception('Not Implemented - update datastore from x to objectStoreHardCodedVersionInteger')
    self.executeInsideTransaction(someFn)


  def _resetDataForTest(self):
    def someFn(connectionContext):
      query = self.objDataTable.delete()
      connectionContext._INT_execute(query)
    self.executeInsideTransaction(someFn)

  def executeInsideConnectionContext(self, fnToExecute):
    context = self._getConnectionContext()
    a = None
    try:
      a = fnToExecute(context)
    finally:
      context._close()
    return a

  #helper function if we need just a single transaction in our contexts
  def executeInsideTransaction(self, fnToExecute):
    def dbfn(context):
      return context.executeInsideTransaction(fnToExecute)
    return self.executeInsideConnectionContext(dbfn)

  def _getConnectionContext(self):
    return ConnectionContext(self)
