# coding:utf8
import datetime, time
from tornado.gen import coroutine, Return
from config.mysql_config import mysql_config
import asynctorndb
from functools import wraps
from collections import deque
from utils.database import AsyncConnectionPool


class BaseModel(object):
  def __init__(self):
    super(BaseModel, self).__init__()
    self.db = AsyncConnectionPool(host=mysql_config['host'], database=mysql_config['database'],
                                  user=mysql_config['user'], passwd=mysql_config['password'],
                                  max_idle_time=2000, max_conn_num=100)

  @property
  def now(self):
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

  @property
  def ts(self):
    return int(time.time())

  @property
  def today(self):
    return datetime.now().strftime("%Y-%m-%d")
