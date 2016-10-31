# -*- coding: utf-8 -*-


class AppError(Exception):

    def __init__(self, err, msg):
        self.code = err
        self.message = msg

    def __str__(self):
        message = self.message
        if isinstance(message, unicode):
            message = message.encode('utf-8')

        return '<%d %s>' % (self.code, message)

# user相关
ErrNoPermission = AppError(1000, u'权限不足')
ErrNoLogin = AppError(10001, u'请先登录')
ErrAddressUserName = AppError(10002, u'收货人名字不能为空')
ErrAddressUserTel = AppError(10002, u'收货人手机不合法')
ErrAddress = AppError(10004, u'收货地址不合法')
ErrUserNoExisted = AppError(10005, u'用户不存在')
ErrUserTel = AppError(10006, u'手机号码不合法')


# deal相关
ErrDealNoExisted = AppError(20001, u'订单不存在')


# article相关
ErrArticleContent = AppError(30001, u'帖子内容不能为空')
ErrOidArticleExisted = AppError(30002, u'该订单已晒')