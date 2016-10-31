# coding:utf8
import datetime, time
from tornado.gen import coroutine, Return
from config.mysql_config import mysql_config
from config.redis_config import redis_config
import asynctorndb
from functools import wraps
from collections import deque
# from utils.database import AsyncConnectionPool
import redis
# from utils.greenify.db_pool import AsyncDBConnection
from utils.database import AsyncConnectionPool

model_db_instance = AsyncConnectionPool(host=mysql_config['host'], database=mysql_config['database'],
                                        user=mysql_config['user'], passwd=mysql_config['password'],
                                        max_idle_time=100, max_conn_num=100)
model_redis_instance = redis.StrictRedis(host=redis_config['host'], port=redis_config['port'], db=5)


class BaseModel(object):
  def __init__(self):
    super(BaseModel, self).__init__()
    self.db = model_db_instance
    self.redis = model_redis_instance

  @property
  def now(self):
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

  @property
  def ts(self):
    return int(time.time())

  @property
  def today(self):
    return datetime.now().strftime("%Y-%m-%d")
