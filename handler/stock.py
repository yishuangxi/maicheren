# coding:utf8
from tornado.gen import coroutine
from handler.base import BaseHandler
from service.stock import StockService


class StockBaseHandler(BaseHandler):
  def __init__(self, *args, **kwargs):
    super(StockBaseHandler, self).__init__(*args, **kwargs)
    self.srv_stock = StockService()


class StockListHandler(StockBaseHandler):
  @coroutine
  def get(self):
    self.json_ok('stock list')


class StockCreateHandler(StockBaseHandler):
  """stock创建"""

  @coroutine
  def post(self):
    vin = self.get_argument('vin')
    model = self.get_argument('model')
    brand_id = self.get_argument('brand_id')
    color_id = self.get_argument('color_id')
    _type = self.get_argument('type')
    seats = self.get_argument('seats')
    displacement = self.get_argument('displacement')
    price = self.get_argument('price')

    data = yield self.srv_stock.create(vin=vin, model=model, brand_id=brand_id, color_id=color_id, _type=_type,
                                       seats=seats, displacement=displacement, price=price)

    self.json_ok(data)


class StockRetrieveHandler(StockBaseHandler):
  """stock查询"""

  @coroutine
  def get(self, stock_id):
    self.json_ok('stock info')


class StockUpdateHandler(StockBaseHandler):
  """stock信息多处修改"""

  def post(self, stock_id):
    self.json_ok('stock Update')


class StockDeleteHandler(StockBaseHandler):
  """stock删除"""

  @coroutine
  def post(self, stock_id):
    self.json_ok('stock delete')


class StockStatusUpdateHandler(StockBaseHandler):
  """stock 仅状态修改"""

  @coroutine
  def post(self, stock_id):
    """库存状态更改"""
    self.json_ok('stock status Update')
