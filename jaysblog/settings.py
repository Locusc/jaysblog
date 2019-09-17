# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 @Time    : 2019/9/17 15:07
 @Author  : Jay Chen
 @FileName: settings.py
 @GitHub  : https://github.com/cRiii
"""
import logging
import os


class BaseConfig(object):

    # 添加mysql数据库的配置
    SQLALCHEMY_DATABASE_URI = "mysql://root:root@127.0.0.1:3306/jaysblog"
    SQLALCHEMY_TRACK_MODIFICATION = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'DDAJDJFQIOWEOWQOQOPTPOFDSJJGJQJJJFJASDJFQIUJAFDAD')


class DevelopmentConfig(BaseConfig):
    """调试模式下的app"""
    DEBUG = True
    LOG_LEVEL = logging.DEBUG


class ProductionConfig(BaseConfig):
    """生产模式下的app"""
    DEBUG = False
    LOG_LEVEL = logging.ERROR


config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig
}
