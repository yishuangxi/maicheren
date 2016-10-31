# coding:utf8
from service.base import BaseService
from tornado.gen import coroutine, Return
from model.stock import StockModel


class StockService(BaseService):
  def __init__(self, *args, **kwargs):
    self.model_stock = StockModel()

  @coroutine
  def create(self, vin='', model='', brand_id='', color_id='', _type='', seats=2, displacement='1.5L', price=1):
    data = yield self.model_stock.create(vin=vin, model=model, brand_id=brand_id, color_id=color_id, _type=_type,
                                         seats=seats, displacement=displacement, price=price)
    raise Return(data)
