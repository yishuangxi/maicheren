#coding=utf-8

import greenify
greenify.greenify()
from greenify import spawn

import logging
import time
import datetime
from collections import deque
from functools import wraps
import itertools
import torndb
import tornado.ioloop
from torndb import Row
from tornado.gen import coroutine, Return
from tornado import locks
from functools import partial
from tornado.options import options


assert greenify.patch_lib("/usr/lib64/mysql/libmysqlclient_r.so")
mutex = locks.Lock()


def enable_debug():
    import inspect
    import greenlet
    import logging

    def trace_green(event, args):
        src, target = args
        if event == "switch":
            logging.info("from %s switch to %s" % (src, target))
        elif event == "throw":
            logging.info("from %s throw exception to %s" % (src, target))
        if src.gr_frame:
            tracebacks = inspect.getouterframes(src.gr_frame)
            buff = []
            for traceback in tracebacks:
                srcfile, lineno, func_name, codesample = traceback[1:-1]
                trace_line = '''File "%s", line %s, in %s\n%s '''
                codesample = "".join(codesample) if codesample else ""
                buff.append(trace_line % (srcfile, lineno, func_name, codesample))

            #logging.info("".join(buff))
            logging.info(buff[0])

    greenlet.settrace(trace_green)
#enable_debug()


class ConnectionError(Exception):
    pass


class TimeoutError(Exception):
    def __init__(self, sql):
        self._msg = sql

    def __str__(self):
        return self._msg


def cov(row):
    return tuple(isinstance(v, (datetime.datetime, datetime.date)) and str(v) or v for v in row)


class Connection(torndb.Connection):

    # add connection timeout    --- added by liuchun
    def __init__(self, pool, *args, **kwargs):
        super(Connection, self).__init__(*args, **kwargs)
        self.tcp_timeout = None
        self.idle_at = time.time()
        self._pool = pool

    def ensure_tcp_timeout(self, timeout=0.8, error=TimeoutError("no sql")):
        # avoiding the unclosed tcp connection
        self.tcp_timeout = self.add_timeout(timeout, error)

    def _on_timeout(self, error):
        self._pool._recycle(self, close=True)
        if error is not None:
            raise error

    def add_timeout(self, seconds, error):
        return tornado.ioloop.IOLoop.current().add_timeout(time.time() + seconds, partial(self._on_timeout, error=error))

    def remove_timeout(self):
        if isinstance(self.tcp_timeout, tornado.ioloop._Timeout):
            tornado.ioloop.IOLoop.current().remove_timeout(self.tcp_timeout)
            self.tcp_timeout = None

    # ---------------------------------------------------------------------------------------------------------------------

    def query(self, query, *parameters, **kwparameters):
        """Returns a row list for the given query and parameters."""
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters, kwparameters)
            column_names = [d[0].lower() for d in cursor.description]
            return [Row(itertools.izip(column_names, cov(row))) for row in cursor]
        finally:
            cursor.close()

    def multi_execute(self, full_sql, *args):
        sql_list = full_sql.split(';')
        if sql_list[-1].strip() == '':
            sql_list = sql_list[:-1]
        offset = 0
        cursor = self._cursor()
        cursor.execute("BEGIN")
        try:
            for sql in sql_list:
                arg_count = sql.count('%s')
                cur_args = args[offset: offset + arg_count]
                cursor.execute(sql, cur_args)  # 不可用 *cur_args ，torndb 这里只接受两个参数
                offset += arg_count
            cursor.execute("COMMIT")
        except Exception as e:
            cursor.execute("ROLLBACK")
        finally:
            cursor.close()


class AsyncDBConnection(object):

    def __init__(self, host, port, database, user, password, charset='utf8', time_zone='+8:00', max_connection=20, idle_time=60):
        self.__host = host
        self.__port = port
        self.__database = database
        self.__user = user
        self.__password = password
        self.__charset = charset
        self.__time_zone = time_zone
        self.__max_connection = max_connection
        self.__idle_time = 60*idle_time  # seconds

        self.__idle_queue = deque()
        self.__busy_queue = deque()

    # add by WuLin
    def disconnect_all(self):
        for conn in self.__idle_queue:
            spawn(conn.close)
        for conn in self.__busy_queue:
            spawn(conn.close)

    @coroutine
    def __get_connection(self, sql):
        # logging.info("in get_conn ==> idle len: %s, busy len: %s" %(len(self.__idle_queue), len(self.__busy_queue)))
        # 直接从空闲队列拿
        if self.__idle_queue:
            c = self.__idle_queue.popleft()
            self.__busy_queue.append(c)
            c.ensure_tcp_timeout(timeout=1, error=TimeoutError(sql))
            raise Return(c)

        yield mutex.acquire()
        cur_conns = len(self.__busy_queue)+len(self.__idle_queue)
        if self.__idle_queue:   # 由于并发情况,__idle_queue必须进行双重检测
            c = self.__idle_queue.popleft()
        elif cur_conns < self.__max_connection:
            c = yield spawn(self.connect)
        else:
            logging.error("connection exceed max:%s" % self.__max_connection)
            mutex.release()
            raise ConnectionError("too many connection")
        self.__busy_queue.append(c)
        c.ensure_tcp_timeout(timeout=1, error=TimeoutError(sql))
        mutex.release()
        raise Return(c)

    def connect(self, *args, **kwargs):
        c = Connection(pool=self, host=self.__host + ':' + str(self.__port), database=self.__database, user=self.__user,
                       password=self.__password, time_zone=self.__time_zone, charset=self.__charset)
        return c

    def __shrink(self):
        for c in list(self.__idle_queue):
            if c.idle_at + self.__idle_time < time.time():
                logging.info("%s idle time out" % c)
                self.__idle_queue.remove(c)
                c.close()
                c = None

    def _recycle(self, c, close=False):
        if c.tcp_timeout:
            c.remove_timeout()
        try:
            self.__busy_queue.remove(c)
            if close:
                c.close()
                c = None
            else:
                c.idle_at = time.time()
                self.__idle_queue.appendleft(c)
            self.__shrink()
        except ValueError:
            logging.error("recycle error, there must be some thing wrong!")

    @coroutine
    def __do_sql(self, method, sql, *args):
        formated_sql = sql + " : " + str(args)
        conn = yield self.__get_connection(formated_sql)
        if hasattr(conn, method):
            try:
                res = yield spawn(getattr(conn, method), sql, *args)  #当超时后,抛出异常,不知为啥后面的流程都不执行了
            except Exception as e:
                raise e
        else:
            logging.error("__do_sql error, method not exist:%s" % method)
        self._recycle(conn)
        raise Return(res)

    def __make_sql_operation(name):
        def __(fn):
            @wraps(fn)
            @coroutine
            def __sql_op(self, sql, *args):
                res = yield self.__do_sql(name, sql, *args)
                raise Return(res)
            return __sql_op
        return __

    @__make_sql_operation("query")
    def query(self):
        pass

    @__make_sql_operation("get")
    def get(self):
        pass

    @__make_sql_operation("insert")
    def insert(self):
        pass

    @__make_sql_operation("execute")
    def execute(self):
        pass

    @__make_sql_operation("multi_execute")  # add by WuLin
    def multi_execute(self):
        pass

    @__make_sql_operation("execute_lastrowid")
    def execute_lastrowid(self):
        pass

    @__make_sql_operation("execute_rowcount")
    def execute_rowcount(self):
        pass

    @__make_sql_operation("executemany")
    def executemany(self):
        pass

    @__make_sql_operation("executemany_lastrowid")
    def executemany_lastrowid(self):
        pass

    @__make_sql_operation("executemany_rowcount")
    def executemany_rowcount(self):
        pass

