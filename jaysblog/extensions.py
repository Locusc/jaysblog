# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 @Time    : 2019/9/17 15:07
 @Author  : Jay Chen
 @FileName: extensions.py
 @GitHub  : https://github.com/cRiii
"""
from flask_script import Manager
from flask_cache import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_login import LoginManager
from flask_redis import FlaskRedis
from flask_wtf import CSRFProtect

db = SQLAlchemy()
manager = Manager()
cache = Cache()
moment = Moment()
login_manager = LoginManager()
redis_store = FlaskRedis()
csrf_protect = CSRFProtect()


@login_manager.user_loader
def load_user(user_id):
    """
        session中只会存储登陆用户的id
        为了获取用户模型类对象 设置用户加载函数
        接收id作为参数 返回对应的用户对象
    """
    from jaysblog.models import UserModel
    user = UserModel.query.get(int(user_id))
    return user
