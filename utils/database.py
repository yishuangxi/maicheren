# coding: utf8
import asynctorndb
from collections import deque
from tornado.gen import coroutine, Return
import time
from functools import wraps, partial
from tornado import ioloop


class ConnectionTimeoutException(Exception):
  """连接超时异常"""

  def __init__(self, value):
    self.value = value

  def __str__(self):
    return repr(self.value)


class ConnectionOverloadException(Exception):
  """连接过载异常"""

  def __init__(self, value="too many connections"):
    self.value = value

  def __str__(self):
    return repr(self.value)


class Connection(asynctorndb.Connection):
  def __init__(self, pool, *args, *kwargs):
    super(Connection, self).__init__(*args, **kwargs)
    self._pool = pool
    self.idle_start_time = time.time()
    self._tcp_timeout = None

  def ensure_tcp_timeout(self, timeout=0.8, error=ConnectionTimeoutException('tcp timeout error')):
    """
    :param timeout: 超时时长
    :param error: 超时的时候，需要报的超时异常对象
    :return:
    """
    self._tcp_timeout = self.add_timeout(timeout, error)

  def add_timeout(self, timeout, error):
    return ioloop.IOLoop.current().add_timeout(time.time() + timeout, partial(self.on_timeout, error=error))

  def on_timeout(self, error):
    self._pool._recycle(self)
    if error is not None:
      raise error

  def remove_timeout(self):
    if isinstance(self._tcp_timeout, ioloop._Timeout):
      ioloop.IOLoop.remove_timeout(self._tcp_timeout)
      self._tcp_timeout = None


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
    self._host = host
    self._database = database
    self._user = user
    self._passwd = passwd
    self._max_idle_time = max_idle_time
    self._max_conn_num = max_conn_num

    self._idle_queue = deque(maxlen=max_conn_num)
    self._busy_queue = deque(maxlen=max_conn_num)

  @coroutine
  def _get_conn(self):
    # 如果busy_queue已经达到最大值了，则抛出已经达到最大连接数异常
    if len(self._busy_queue) >= self._max_conn_num:
      raise ConnectionOverloadException()

    # 如果idle_queue为空，则新创建一个conn，并将其放入idle_queue
    if len(self._idle_queue) == 0:
      conn = yield self._generate_conn()
      self._idle_queue.append(conn)

    # 从idle_queue取数据，并塞到busy_queue里面去
    conn = self._idle_queue.popleft()
    self._busy_queue.append(conn)

    # 返回连接
    raise Return(conn)

  @coroutine
  def _generate_conn(self):
    #这里把self传入，则在conn中可以通过conn._pool引用到该pool对象
    conn = Connection(self, host=self._host, database=self._database, user=self._user, passwd=self._passwd)

    yield conn.connect()
    raise Return(conn)

  def _recycle_conn(self, conn):
    """回收连接"""
    self._busy_queue.remove(conn)
    #重置一下conn的idle_start_time属性
    conn.idle_start_time = time.time()
    self._idle_queue.append(conn)

  def _release_idle_conn(self):
    """释放空闲时间太长的连接"""
    for conn in self._idle_queue:
      if time.time() - conn.idle_start_time > self._max_idle_time:
        self._idle_queue.remove(conn)
        conn.close()

  @coroutine
  def __do_sql(self, method, sql, *args, **kwargs):
    conn = yield self._get_conn()
    if hasattr(conn, method):
      method = getattr(conn, method)
      res = yield method(sql, *args, **kwargs)
      #用完了conn，记得回收
      self._recycle_conn(conn)
      #顺便释放空闲连接
      self._release_idle_conn()
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
