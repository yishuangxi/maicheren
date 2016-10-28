# coding: utf8
import asynctorndb
from collections import deque
from tornado.gen import coroutine, Return
import time
from functools import wraps


class ConnectionOverloadException(Exception):
  """连接过载异常"""

  def __init__(self, value="too many connections"):
    self.value = value

  def __str__(self):
    return repr(self.value)


class AsyncConnectionPool(object):
  """异步连接池"""

  def __init__(self, host, database, user, passwd, max_idle_time=2000, max_conn_num=100):
    """
    :param host:
    :param database:
    :param user:
    :param passwd:
    :param max_idle_time: 连接最大空闲时间，单位为秒
    :param max_conn_num: 最大连接数
    """
    super(AsyncConnectionPool, self).__init__()
    self.__host = host
    self.__database = database
    self.__user = user
    self.__passwd = passwd
    self.__max_idle_time = max_idle_time
    self.__max_conn_num = max_conn_num

    self.__idle_queue = deque(maxlen=max_conn_num)
    self.__busy_queue = deque(maxlen=max_conn_num)

  @coroutine
  def __get_conn(self):
    # 如果busy_queue已经达到最大值了，则抛出已经达到最大连接数异常
    if len(self.__busy_queue) == self.__max_conn_num:
      raise ConnectionOverloadException()

    # 如果idle_queue为空，则新创建一个conn，并将其放入idle_queue
    if len(self.__idle_queue) == 0:
      conn = yield self.__generate_conn()
      self.__idle_queue.append(conn)

    # 从idle_queue取数据，并塞到busy_queue里面去
    conn = self.__idle_queue.popleft()
    self.__busy_queue.append(conn)

    # 返回连接
    raise Return(conn)

  @coroutine
  def __generate_conn(self):
    conn = asynctorndb.Connection(host=self.__host, database=self.__database, user=self.__user, passwd=self.__passwd)
    yield conn.connect()
    raise Return(conn)

  def __recycle_conn(self, conn):
    """回收连接"""
    self.__busy_queue.remove(conn)
    self.__idle_queue.append(conn)

  def __release_idle_conn(self):
    """释放空闲时间太长的连接"""
    for conn in self.__idle_queue:
      if time.time() - conn.idle_start_time > self.__max_idle_time:
        self.__idle_queue.remove(conn)
        conn.close()

  @coroutine
  def __do_sql(self, method, sql, *args, **kwargs):
    conn = yield self.__get_conn()
    if hasattr(conn, method):
      method = getattr(conn, method)
      res = yield method(sql, *args, **kwargs)
      self.__recycle_conn(conn)
      raise Return(res)

  # 装饰器，装饰asynctorndb各方法：iter, query, get, update, delete, execute, insert,
  def __do_sql_operation(method):
    def _(func):
      @wraps(func)
      @coroutine
      def __(self, sql, *args, **kwargs):
        res = yield self.__do_sql(method, sql, *args, **kwargs)
        raise Return(res)

      return __

    return _

  @__do_sql_operation('iter')
  def iter(self):
    pass

  @__do_sql_operation('query')
  def query(self):
    pass

  @__do_sql_operation('get')
  def get(self):
    pass

  @__do_sql_operation('execute')
  def execute(self):
    pass

  @__do_sql_operation('execute_lastrowid')
  def execute_lastrowid(self):
    pass

  @__do_sql_operation('execute_rowcount')
  def execute_rowcount(self):
    pass

  @__do_sql_operation('executemany')
  def executemany(self):
    pass

  @__do_sql_operation('executemany_lastrowid')
  def executemany_lastrowid(self):
    pass

  @__do_sql_operation('executemany_rowcount')
  def executemany_rowcount(self):
    pass

  @__do_sql_operation('update')
  def update(self):
    pass

  @__do_sql_operation('delete')
  def delete(self):
    pass

  @__do_sql_operation('updatemany')
  def updatemany(self):
    pass

  @__do_sql_operation('insert')
  def insert(self):
    pass

  @__do_sql_operation('insertmany')
  def insertmany(self):
    pass
