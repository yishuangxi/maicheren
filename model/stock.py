# coding:utf8

from model.base import BaseModel
from tornado.gen import coroutine, Return


class StockModel(BaseModel):
  @coroutine
  def create(self, vin='', model='', brand_id='', color_id='', _type='', seats=2, displacement='1.5L', price=1):
    status = 'selling'
    sql = '''insert into stock value (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    data = yield self.db.execute(sql, vin, model, brand_id, color_id, _type, seats, displacement, price, status)

    raise Return(data)

  @coroutine
  def find_one_by(self, field, value):
    pass

  @coroutine
  def find_list_by(self):
    pass

  @coroutine
  def find_page_by(self, before_id):
    pass
