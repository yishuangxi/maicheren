# coding:utf8
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

from base import BaseHandler


class IndexHandler(BaseHandler):
  def get(self):
    self.render('index.html')
