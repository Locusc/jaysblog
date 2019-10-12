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

import click
from flask import Flask
from flask_wtf.csrf import generate_csrf
from jaysblog.extensions import db, manager, cache, moment, login_manager, redis_store, csrf_protect
from jaysblog.models import User, Category, Comment, Reply, Post
from jaysblog.settings import config
from jaysblog.blueprints.auth.auth_blueprint import auth_bp
from jaysblog.blueprints.admin.admin_blueprint import admin_bp
from jaysblog.blueprints.blog.blog_blueprint import blog_bp
from jaysblog.blueprints.user.user_blueprint import user_bp
from jaysblog.blueprints.blog.journey_blueprint import journey_bp
from jaysblog.fakes import fake_categories, fake_comment, fake_posts, fake_replies, fake_admin, fake_user,fake_journey


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    register_logging(app, config_name)  # 注册日志处理器
    register_blueprints(app)  # 注册蓝图
    register_errors(app)  # 注册错误处理器
    register_extensions(app)  # 注册扩展(扩展初始化)
    register_shell_context(app)  # 注册shell上下文处理函数
    register_commands(app)  # 注册自定义命令
    register_csrf(app)  # 注册令牌

    """
        如果忘记返回app实例
        报错:
            flask.cli.NoAppException: 
            Failed to find Flask application or factory in module "jaysblog". Use "FLASK_APP=jaysblog:name to specify one.
        找不到jaysblog模块
    """
    return app


def register_shell_context(app):
    """
        将对象和模块类导入到Python上下文中
        可以在命令行shell中直接使用 不需要import
    """
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, User=User, Category=Category, Comment=Comment, Reply=Reply, Post=Post)


def register_extensions(app):
    db.init_app(app)
    # cache.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    redis_store.init_app(app)
    csrf_protect.init_app(app)


def register_blueprints(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(journey_bp, url_prefix='/journey')


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


def register_csrf(app):
    # 保护除GET以外的请求  在GET请求时创建令牌
    # 将token放入到cookie中 请求时需要在请求头中获取并返回给后台
    @app.after_request
    def set_csrf_token(response):
        csrf_token = generate_csrf()
        response.set_cookie("csrf_token", csrf_token)
        return response


def register_logging(app, config_name):
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


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initDataBase(drop):
        """初始化数据库"""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?')
            db.drop_all()
            click.echo('Drop tables')
        db.create_all()
        click.echo('Initialized database.')

    """
        prompt:
            如果用户没有输入 以提示符的形式请求输入
            设置为True默认会使用选项值得首字母大写形式作为提示字符
            提示字符也可以显示使用prompt参数传入
        confirmation_prompt:
            设置为True来进行二次确认输入 确保两次密码输入匹配
        hide_input：
            设置为True隐藏输入内容
    """
    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login')
    @click.option('--password', prompt=True, help='The password used to login',
                  confirmation_prompt=True, hide_input=True)
    def init(username, password):
        click.echo('Initializing the database')
        db.create_all()

        user = User.query.first()
        if user is not None:
            click.echo('The administrator already exists, updating...')
            user.nick_name = username
            user.password = password
        else:
            click.echo('Creating the temporary administrator account...')
            user = User()
            user.nick_name = username,
            user.mobile = '13888888888',
            user.is_admin = True,
            user.password = password
            db.session.add(user)

        category = Category.query.first()
        if category is None:
            click.echo('Creating the default category...')
            category = Category()
            category.cg_name = 'Default'

        db.session.commit()
        click.echo('done')

    @app.cli.command()
    @click.option('--user', default=50, help='Quantity of users, default is 50.')
    @click.option('--category', default=10, help='Quantity of categories, default is 10.')
    @click.option('--post', default=50, help='Quantity of posts, default is 50.')
    @click.option('--comment', default=500, help='Quantity of comments, default is 500.')
    @click.option('--reply', default=1000, help='Quantity of reply, default is 1000.')
    @click.option('--journey', default=20, help='Quantity of journey, default is 20.')
    def forge(user, category, post, comment, reply, journey):
        """Generate fake data."""
        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator.')
        fake_admin()

        click.echo('Generating the users %s.' % user)
        fake_user(user)

        click.echo('Generating the categories %s.' % category)
        fake_categories(category)

        click.echo('Generating the posts %s.' % post)
        fake_posts(post)

        click.echo('Generating the comments %s.' % comment)
        fake_comment(comment)

        click.echo('Generating the replies %s.' % reply)
        fake_replies(reply)

        click.echo('Generating the journey %s.' % journey)
        fake_journey(journey)

        click.echo('done')



