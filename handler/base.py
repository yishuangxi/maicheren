# coding:utf8
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

import json, datetime, time
from tornado.web import RequestHandler


class DatetimeEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, datetime.datetime):
      encoded_object = time.mktime(obj.timetuple())
    else:
      encoded_object = json.JSONEncoder.default(self, obj)
    return encoded_object


class BaseHandler(RequestHandler):
  def json_ok(self, data={}):
    self.set_header('content-type', 'application/json')
    self.write({
      'code': 0,
      'data': self.__json(data)
    })

  def json_err(self, msg='', code=1):
    self.set_header('content-type', 'application/json')
    self.write({
      'code': code,
      'msg': msg
    })

  def __json(self, data):
    return json.loads(self.__dumps(data))

  def __dumps(self, data):
    return json.dumps(data, cls=DatetimeEncoder)
