# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 @Time    : 2019/9/23 13:48
 @Author  : Jay Chen
 @FileName: fakes.py
 @GitHub  : https://github.com/cRiii
 @Desc    : 虚拟数据文件
"""
import random
from faker import Faker

from sqlalchemy.exc import IntegrityError
from jaysblog import db
from jaysblog.models import Comment, Category, User, Post, Reply

fake = Faker()


# 增加虚拟用户
def fake_user():
    user = User()
    user.nick_name = 'JayChen'
    user.password = '123456'
    user.mobile = '13688888888'
    user.email = '2227628925@qq.com'
    db.session.add(user)
    db.session.commit()


# 增加虚拟分类
def fake_categories(count=10):
    category = Category()
    category.cg_name = 'Default'

    for i in range(count):
        category = Category()
        category.cg_name = fake.word()
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


# 增加虚拟文章
def fake_posts(count=50):
    post = Post()
    for i in range(count):
        post.post_title = fake.sentence()
        post.post_user_id = User.query.get(1)
        post.post_content = fake.text(2000)
        post.post_category_id = Category.query.get(random.randint(1, Category.query.count()))
        db.session.add(post)

    db.session.commit()


# 增加虚拟评论
def fake_comment(count=300):
    pass


