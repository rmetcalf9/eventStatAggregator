from sqlalchemy import select, and_, func
import datetime


def collectStats(tenant, name, subname, start, end, queryContext):
  if subname is not None:
    raise Exception("Not implemented")

  stmt = select([
    queryContext.mainFactory.objDataTable.c.year,
    queryContext.mainFactory.objDataTable.c.month,
    queryContext.mainFactory.objDataTable.c.dom,
    func.count(queryContext.mainFactory.objDataTable.c.event_name)
  ]
    ,whereclause=(
      and_(
        queryContext.mainFactory.objDataTable.c.tenant == tenant
        ,queryContext.mainFactory.objDataTable.c.event_name == name
        #TODO ADD DATE RANGE CLAUSE HERE
      )
    )
  ).select_from(queryContext.mainFactory.objDataTable).group_by(
    queryContext.mainFactory.objDataTable.c.event_name,
    queryContext.mainFactory.objDataTable.c.year,
    queryContext.mainFactory.objDataTable.c.month,
    queryContext.mainFactory.objDataTable.c.dom
  )

  # stmt = select([
  #   queryContext.mainFactory.objDataTable.c.event_name,
  #   queryContext.mainFactory.objDataTable.c.year,
  #   queryContext.mainFactory.objDataTable.c.month,
  #   queryContext.mainFactory.objDataTable.c.dom
  # ])

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
    curDay = str(curDate.year) + str(curDate.month) + str(curDate.day)
    print("CURDATE", curDate, curDay)
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