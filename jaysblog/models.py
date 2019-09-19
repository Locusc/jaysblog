# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 @Time    : 2019/9/17 15:07
 @Author  : Jay Chen
 @FileName: models.py
 @GitHub  : https://github.com/cRiii
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from jaysblog.extensions import db
from flask_login import UserMixin


class BaseModel(object):
    # 模型基类 为所有模型添加创建和更新的时间
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class UserModel(BaseModel, db.Model, UserMixin):
    """
        UserMixin表示通过认证的用户
            is_authenticated 表示用户已通过认证 返回True 否则False
            is_active 表示允许用户登陆 返回True 否则False
            is_anonymous 表示如果当前未用户登陆(匿名用户) 返回True 否则False
            get_id() 以unicode形式返回用户唯一标识
    """
    __tablename__ = 'b_users'

    id = db.Column(db.Integer, primary_key=True)  # 用户id
    nick_name = db.Column(db.String(32), unique=True, nullable=False)  # 用户名
    password_hash = db.Column(db.String(128), nullable=False)  # 用户密码
    mobile = db.Column(db.String(11), unique=True, nullable=False)  # 手机号码
    email = db.Column(db.String(64), unique=True, nullable=True)  # 邮箱
    desc = db.Column(db.String(256))  # 个人简介
    avatar_url = db.Column(db.String(256))  # 用户头像路径
    is_admin = db.Column(db.Boolean, default=False)  # 是否为管理员
    last_login_time = db.Column(db.DateTime, default=datetime.now)  # 最后一次登陆时间
    is_delete = db.Column(db.Integer, default=0)  # 用户是否被删除
    gender = db.Column(
        db.Enum(
            'MAN',  # 男
            'WOMAN'  # 女
        ), default='MAN'
    )

    @property
    def password(self):
        raise AttributeError(u'该属性不可读')

    @password.setter
    def password(self, value):
        """
            generate_password_hash（password，method='pbkdf2：sha256'，salt_length=8）
                method指定计算散列值的方法
                salt_length 指定盐长度
        """
        self.password_hash = generate_password_hash(value)

    def check_password(self, password):
        """
            接收散列值 和 密码作比较 返回布尔类型
            check_password_hash（pwhash，password）
        """
        return check_password_hash(self.password_hash, password)


