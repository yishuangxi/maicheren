# coding:utf8
from tornado.gen import coroutine
from handler.base import BaseHandler


class SkuListHandler(BaseHandler):
  @coroutine
  def get(self):
    self.json_ok('Sku list')


class SkuCreateHandler(BaseHandler):
  """Sku创建"""

  @coroutine
  def post(self):
    self.json_ok('Sku add')


class SkuRetrieveHandler(BaseHandler):
  """Sku查询"""

  @coroutine
  def get(self, Sku_id):
    self.json_ok('Sku info')


class SkuUpdateHandler(BaseHandler):
  """Sku信息多处修改"""

  def post(self, Sku_id):
    self.json_ok('Sku Update')


class SkuDeleteHandler(BaseHandler):
  """Sku删除"""

  @coroutine
  def post(self, Sku_id):
    self.json_ok('Sku delete')


class SkuStatusUpdateHandler(BaseHandler):
  """Sku 仅状态修改"""

  @coroutine
  def post(self, Sku_id):
    """库存状态更改"""
    self.json_ok('Sku status Update')
