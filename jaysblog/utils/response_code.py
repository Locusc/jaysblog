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

    USER_LOGIN_ERROR = 3001
    USER_LOGOUT_ERROR = 3002
    USER_NOT_EXIST = 3003
    USER_PASSWORD_ERROR = 3004

    DATABASE_COMMIT_ERROR = 4001
    DATABASE_SELECT_ERROR = 4002


    # DBERR = 4001
    # NODATA = 4002
    # DATAEXIST = 4003
    # DATAERR = 4004
    # SESSIONERR = 4101
    # LOGINERR = 4102
    # PARAMERR = 4103
    # USERERR = 4104
    # ROLEERR = 4105
    # PWDERR = 4106
    # REQERR = 4201
    # IPERR = 4202
    # THIRDERR = 4301
    # IOERR = 4302
    # SERVERERR = 4500
    # UNKOWNERR = 4501


error_map = {
    RET.OK: u"成功",

    RET.PARAMS_MISSING_ERROR: u"参数缺失错误",

    RET.USER_LOGIN_ERROR: u"用户登陆失败",
    RET.USER_LOGOUT_ERROR: u"用户退出失败",
    RET.USER_NOT_EXIST: u"用户不存在",
    RET.USER_PASSWORD_ERROR: u"用户密码错误",

    RET.DATABASE_SELECT_ERROR: u"数据库查询失败",
    RET.DATABASE_COMMIT_ERROR: u"数据库提交失败",

    # RET.DBERR: u"数据库查询错误",
    # RET.NODATA: u"无数据",
    # RET.DATAEXIST: u"数据已存在",
    # RET.DATAERR: u"数据错误",
    # RET.SESSIONERR: u"用户未登录",
    # RET.LOGINERR: u"用户登录失败",
    # RET.PARAMERR: u"参数错误",
    # RET.USERERR: u"用户不存在或未激活",
    # RET.ROLEERR: u"用户身份错误",
    # RET.PWDERR: u"密码错误",
    # RET.REQERR: u"非法请求或请求次数受限",
    # RET.IPERR: u"IP受限",
    # RET.THIRDERR: u"第三方系统错误",
    # RET.IOERR: u"文件读写错误",
    # RET.SERVERERR: u"内部错误",
    # RET.UNKOWNERR: u"未知错误",
}