# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 @Time    : 2019/9/17 15:01
 @Author  : Jay Chen
 @FileName: response_code.py
 @GitHub  : https://github.com/cRiii
"""


class RET:
    OK = 200

    PARAMS_MISSING_ERROR = 2001
    IMAGE_CODE_OVERDUE_ERROR = 2002
    IMAGE_CODE_INPUT_ERROR = 2003

    USER_LOGIN_ERROR = 3001
    USER_LOGOUT_ERROR = 3002
    USER_NOT_EXIST = 3003
    USER_PASSWORD_ERROR = 3004
    USER_LOCK_ERROR = 3005
    USER_REGISTER_ERROR = 3006
    USER_OAUTH_ERROR = 3007

    DATABASE_COMMIT_ERROR = 4001
    DATABASE_SELECT_ERROR = 4002

    REDIS_SAVE_ERROR = 4011
    REDIS_GET_ERROR = 4012


error_map = {
    RET.OK: u"成功",

    RET.PARAMS_MISSING_ERROR: u"参数缺失错误",
    RET.IMAGE_CODE_OVERDUE_ERROR: u"图片验证码过期错误",
    RET.IMAGE_CODE_INPUT_ERROR: u"图片验证码输入错误",

    RET.USER_LOGIN_ERROR: u"用户登陆失败",
    RET.USER_LOGOUT_ERROR: u"用户退出失败",
    RET.USER_NOT_EXIST: u"用户不存在",
    RET.USER_PASSWORD_ERROR: u"用户密码错误",
    RET.USER_LOCK_ERROR: u"锁定用户",
    RET.USER_REGISTER_ERROR: u"用户注册错误",
    RET.USER_OAUTH_ERROR: u"用户第三方认证错误",

    RET.DATABASE_SELECT_ERROR: u"数据库查询失败",
    RET.DATABASE_COMMIT_ERROR: u"数据库提交失败",

    RET.REDIS_SAVE_ERROR: u'REDIS保存数据失败',
    RET.REDIS_GET_ERROR: u'REDIS获取数据失败',
}
