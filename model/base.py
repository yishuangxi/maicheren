# coding:utf8
import datetime, time


class BaseModel(object):
  @property
  def now(self):
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

  @property
  def ts(self):
    return int(time.time())

  @property
  def today(self):
    return datetime.now().strftime("%Y-%m-%d")
