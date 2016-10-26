# coding:utf8
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

from base import BaseHandler

class IndexHandler(BaseHandler):
  def get(self):
    name = 'yanshanshan'
    friends = ['yishuangxi', 'yanpengfei', 'yiye', 'weihong']
    user_info = {
      'name': 'yishuangxi',
      'id': 1,
      'sex': 'male',
      'age': 30
    }
    self.render('index.html')

  def post(self, *args, **kwargs):
    self.write('this is post in index page')
