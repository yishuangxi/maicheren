# coding:utf8
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.autoreload
from tornado.options import options, define

define("port", default=8888, help="run on the given port", type=int)
define('application_name', default='taiqiuabc', type=str)
define('debug', default=False, type=bool)
tornado.options.parse_command_line()

from config.app_config import settings
from router import handlers


def release():
  print 'release'


def create_app():
  return tornado.web.Application(handlers, **settings)


def main():
  http_server = tornado.httpserver.HTTPServer(create_app(), xheaders=True)
  http_server.listen(options.port)
  print 'http server listening on ', options.port
  io_loop = tornado.ioloop.IOLoop.instance()
  tornado.autoreload.add_reload_hook(release)
  io_loop.start()


if __name__ == '__main__':
  main()
