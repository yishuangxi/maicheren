# coding:utf8
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

from base import BaseHandler
import json


class UserHandler(BaseHandler):
  def get(self):
    user_info = {
      'name': 'yishuangxi',
      'id': 1,
      'sex': 'male',
      'age': 30
    }
    self.render('user.html', user_info=user_info)
    # self.write('this is get in user page')

  def post(self, *args, **kwargs):
    self.write('this is post in user page')


class UserInfoApiHandler(BaseHandler):
  def get(self):
    user_info = {
      'name': 'yishuangxi',
      'id': 1,
      'sex': 'male',
      'age': 30
    }
    self.json_ok(user_info)
