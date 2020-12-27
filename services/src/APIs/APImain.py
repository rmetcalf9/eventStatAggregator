from flask import request
from flask_restplus import Resource, fields, marshal
from werkzeug.exceptions import BadRequest, Conflict, InternalServerError, NotFound, Forbidden
import Logic

def getStatsEndpointModel(appObj):
  return appObj.flastRestPlusAPIObject.model('statsEndpointModel', {
    'start': fields.DateTime(dt_format=u'iso8601', description='Start Date (time part ignored)'),
    'end': fields.DateTime(dt_format=u'iso8601', description='End Date (time part ignored)')
  })

def getStatsResultModel(appObj):
  dailyResultModel = appObj.flastRestPlusAPIObject.model('dailyResultModel', {
    'daynum': fields.Integer(default=None, description='Sortable day number'),
    'date': fields.String(default='DEFAULT', description='Date in form YYYYMMDD'),
    'count': fields.Integer(default=None, description='Event count for this day')
  })
  return appObj.flastRestPlusAPIObject.model('statsResultModel', {
    'daily': fields.List(fields.Nested(dailyResultModel))
  })

def requiredInPayload(content, fieldList):
  for a in fieldList:
    if a not in content:
      raise BadRequest(a + ' not in payload')
    if content[a] is None:
      raise BadRequest(a + ' should not be empty')

def registerAPI(appObj, APInamespace):

  @APInamespace.route('/statsA/<string:tenant>/<string:name>')
  class statsName(Resource):
    '''stats'''

    @APInamespace.doc('Returns Stats')
    @APInamespace.expect(getStatsEndpointModel(appObj))
    @appObj.flastRestPlusAPIObject.response(400, 'Validation error')
    @appObj.flastRestPlusAPIObject.response(200, 'Success')
    @appObj.flastRestPlusAPIObject.marshal_with(getStatsResultModel(appObj), code=200, description='Stats lookedup', skip_none=True)
    @APInamespace.response(403, 'Forbidden - User does not have required role')
    def post(self, tenant, name):
      '''Get Stats'''
      content_raw = request.get_json()
      content = marshal(content_raw, getStatsEndpointModel(appObj))
      requiredInPayload(content, ['start', 'end'])


      def dbfn(queryContext):
        return Logic.collectStats(
          tenant=tenant,
          name=name,
          subname=None,
          start=content["start"],
          end=content["end"],
          queryContext=queryContext
        )
      try:
        return appObj.objectStore.executeInsideConnectionContext(dbfn)
      except Exception as err:
        raise err

      return collectStats(tenant, name, subname, start, end, queryConnection)

