from sqlalchemy import select, and_, func



def collectStats(tenant, name, subname, start, end, queryContext):
  if subname is not None:
    raise Exception("Not implemented")

  stmt = select([
    queryContext.mainFactory.objDataTable.c.event_name,
    queryContext.mainFactory.objDataTable.c.year,
    queryContext.mainFactory.objDataTable.c.month,
    queryContext.mainFactory.objDataTable.c.dom,
    func.count(queryContext.mainFactory.objDataTable.c.event_name)
  ],
    whereclause=(
      and_(
        queryContext.mainFactory.objDataTable.c.tenant == tenant,
        queryContext.mainFactory.objDataTable.c.event_name == name
      )
    )
  ).select_from(queryContext.mainFactory.objDataTable).group_by(
    queryContext.mainFactory.objDataTable.c.event_name,
    queryContext.mainFactory.objDataTable.c.year,
    queryContext.mainFactory.objDataTable.c.month,
    queryContext.mainFactory.objDataTable.c.dom
  )

  dailyResultList = []

  retVal = {
    "daily": dailyResultList
  }

  return retVal, 200