# coding:utf8
from handler.index import IndexHandler
from handler.user import UserHandler, UserInfoApiHandler

handlers = [
  (r'/', IndexHandler),
  (r'/u', UserHandler),
  (r'/api/u/info', UserInfoApiHandler)
]
