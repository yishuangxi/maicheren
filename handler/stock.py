# coding:utf8
from tornado.gen import coroutine
from handler.base import BaseHandler


class StockListHandler(BaseHandler):
  @coroutine
  def get(self):
    self.json_ok('stock list')


class StockCreateHandler(BaseHandler):
  """stock创建"""

  @coroutine
  def post(self):
    self.json_ok('stock add')


class StockRetrieveHandler(BaseHandler):
  """stock查询"""

  @coroutine
  def get(self, stock_id):
    self.json_ok('stock info')


class StockUpdateHandler(BaseHandler):
  """stock信息多处修改"""

  def post(self, stock_id):
    self.json_ok('stock Update')


class StockDeleteHandler(BaseHandler):
  """stock删除"""

  @coroutine
  def post(self, stock_id):
    self.json_ok('stock delete')


class StockStatusUpdateHandler(BaseHandler):
  """stock 仅状态修改"""

  @coroutine
  def post(self, stock_id):
    """库存状态更改"""
    self.json_ok('stock status Update')
