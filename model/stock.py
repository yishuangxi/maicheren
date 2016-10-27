# coding:utf8

from Model.base import BaseModel
from tornado.gen import coroutine, Return


class StockModel(BaseModel):
  @coroutine
  def get_one_by(self, field, value):
    pass

  @coroutine
  def get_page_by(self, before_id):
    pass
