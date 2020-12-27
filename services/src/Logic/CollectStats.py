from sqlalchemy import select, and_, func
import datetime


def getStatement(tenant, name, subname, start, end, queryContext):
  dayAfterEnd = end + datetime.timedelta(days=1)

  if subname is not None:
    return select([
      queryContext.mainFactory.objDataTable.c.year,
      queryContext.mainFactory.objDataTable.c.month,
      queryContext.mainFactory.objDataTable.c.dom,
      func.count(queryContext.mainFactory.objDataTable.c.event_name)
    ]
      , whereclause=(
        and_(
          queryContext.mainFactory.objDataTable.c.tenant == tenant
          , queryContext.mainFactory.objDataTable.c.event_name == name
          , queryContext.mainFactory.objDataTable.c.event_subname == subname
          , queryContext.mainFactory.objDataTable.c.event_date >= start
          , queryContext.mainFactory.objDataTable.c.event_date <= dayAfterEnd
        )
      )
    ).select_from(queryContext.mainFactory.objDataTable).group_by(
      queryContext.mainFactory.objDataTable.c.event_name,
      queryContext.mainFactory.objDataTable.c.event_subname,
      queryContext.mainFactory.objDataTable.c.year,
      queryContext.mainFactory.objDataTable.c.month,
      queryContext.mainFactory.objDataTable.c.dom
    )

  return select([
    queryContext.mainFactory.objDataTable.c.year,
    queryContext.mainFactory.objDataTable.c.month,
    queryContext.mainFactory.objDataTable.c.dom,
    func.count(queryContext.mainFactory.objDataTable.c.event_name)
  ]
    ,whereclause=(
      and_(
        queryContext.mainFactory.objDataTable.c.tenant == tenant
        ,queryContext.mainFactory.objDataTable.c.event_name == name
        ,queryContext.mainFactory.objDataTable.c.event_date >= start
        , queryContext.mainFactory.objDataTable.c.event_date <= dayAfterEnd
      )
    )
  ).select_from(queryContext.mainFactory.objDataTable).group_by(
    queryContext.mainFactory.objDataTable.c.event_name,
    queryContext.mainFactory.objDataTable.c.year,
    queryContext.mainFactory.objDataTable.c.month,
    queryContext.mainFactory.objDataTable.c.dom
  )

def collectStats(tenant, name, subname, start, end, queryContext):
  stmt = getStatement(tenant=tenant, name=name, subname=subname, start=start, end=end, queryContext=queryContext)

  result = queryContext._INT_executeQuery(stmt)
  resultDict = {}
  for row in result:
    year=row[0]
    month=row[1]
    dom=row[2]
    count=row[3]
    ## print("row", year, month, dom, count)
    resultDict[str(year) + str(month) + str(dom)] = count

  # Loop over every day in range inclusive of start and end
  dailyResultList = []
  curDate = start
  seq = 0
  while curDate <= end:
    count = 0
    curDay = "{:04d}".format(curDate.year) + "{:02d}".format(curDate.month) + "{:02d}".format(curDate.day)
    if curDay in resultDict:
      count = resultDict[curDay]
    seq += 1
    obj = {
      "daynum": seq,
      "date": curDay,
      "count": count
    }
    dailyResultList.append(obj)

    curDate = curDate + datetime.timedelta(days=1)

  retVal = {
    "daily": dailyResultList
  }

  return retVal, 200