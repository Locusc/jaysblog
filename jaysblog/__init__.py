# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 @Time    : 2019/9/17 15:07
 @Author  : Jay Chen
 @FileName: __init__.py
 @GitHub  : https://github.com/cRiii
"""
import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask, jsonify
from jaysblog.extensions import SQLAlchemy
from jaysblog.settings import config
from jaysblog.blueprints.auth import auth_bp


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('jaysblog')
    app.config.from_object(config[config_name])

    register_logging(config_name, app)  # 注册日志处理器
    register_blueprints(app)  # 注册蓝图
    register_errors(app)  # 注册错误处理器

    """
        如果忘记返回app实例
        报错:
            flask.cli.NoAppException: 
            Failed to find Flask application or factory in module "jaysblog". Use "FLASK_APP=jaysblog:name to specify one.
        找不到jaysblog模块
    """
    return app


def register_logging(config_name, app):
    # 在__init__.create_app(config_name)设置了日志的记录等级
    # 调试debug级
    logging.basicConfig(level=config[config_name].LOG_LEVEL)
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/jaysblog.log", maxBytes=10 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    """
        app.debug 属性存储用来判断程序是否开启了调试模式的布尔值
        当FLASK_ENV环境变量的值为development时
        app.debug会返回True 否则返回False
        可以通过app.env属性获取FLASK_ENV的设置值
    """
    if not app.debug:
        # 为全局的日志工具对象（flask app使用的）添加日志记录器
        logging.getLogger().addHandler(file_log_handler)


def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')


def register_errors(app):
    # @app.errorhandler(404)
    # def page_not_found(e):
    #     return jsonify({
    #         'code': e.code,
    #         'description': e.description,
    #         'messages': str(e)
    #     })
    #
    # @app.errorhandler([404, 500])
    # def page_not_found(e):
    #     return jsonify({
    #         'code': e.code,
    #         'description': e.description,
    #         'messages': str(e)
    #     })
    pass


