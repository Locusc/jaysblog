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
from jaysblog.models import Comment, Category, User, Post, Reply, Journey
from jaysblog.utils.tools import random_mobile

fake = Faker()


# 增加管理员
def fake_admin():
    user = User()
    user.nick_name = 'JayChen'
    user.password = '123456'
    user.mobile = '13688888888'
    user.email = '2227628925@qq.com'
    user.is_admin = True
    db.session.add(user)
    db.session.commit()


# 增加虚拟用户
def fake_user(count=50):
    gender = ('MAN', 'WOMAN')
    for i in range(count):
        user = User()
        user.nick_name = fake.name()
        user.password = '123456'
        user.mobile = random_mobile()
        user.email = fake.email()
        user.is_admin = False
        user.gender = random.choice(gender)
        db.session.add(user)
    db.session.commit()


# 增加虚拟分类
def fake_categories(count=10):
    category = Category()
    category.cg_name = 'Default'
    db.session.add(category)

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
    for i in range(count):
        post = Post()
        post.post_title = fake.sentence()
        post.post_user_id = User.query.get(1).id
        post.post_content = fake.text(2000)
        post.post_digest = fake.text(200)
        post.post_category_id = random.randint(1, Category.query.count())
        db.session.add(post)

    db.session.commit()


# 增加虚拟评论
def fake_comment(count=500):
    # 增加已审批过的评论
    for i in range(count):
        comment = Comment()
        comment.comment_user_id = random.randint(1, Category.query.count())
        comment.comment_content = fake.sentence()
        comment.comment_post_id = random.randint(1, Post.query.count())
        comment.comment_status = 1
        db.session.add(comment)

    # 增加审核未通过的评论和管理员评论
    salt = int(count * 0.1)
    for i in range(salt):
        comment = Comment()
        comment.comment_user_id = random.randint(1, Category.query.count())
        comment.comment_content = fake.sentence()
        comment.comment_post_id = random.randint(1, Post.query.count())
        comment.comment_status = 0
        db.session.add(comment)

        comment = Comment()
        comment.comment_user_id = random.randint(1, Category.query.count())
        comment.comment_content = fake.sentence()
        comment.comment_post_id = random.randint(1, Post.query.count())
        comment.comment_status = 1
        comment.comment_from_admin = 1
        db.session.add(comment)
    db.session.commit()


# 增加虚拟回复
def fake_replies(count=1000):
    user_name_list = User.query.with_entities(User.nick_name).all()
    for i in range(count):
        reply = Reply()
        reply.reply_content = fake.sentence()
        reply.reply_comment_id = random.randint(1, Comment.query.count())
        reply.reply_from_user = random.choice(user_name_list)[0]
        reply.reply_to_user = random.choice(user_name_list)[0]
        reply.reply_status = 1
        db.session.add(reply)

    db.session.commit()


def fake_journey(count=20):
    for i in range(count):
        journey = Journey()
        journey.journey_desc = fake.sentence()
        journey.journey_title = fake.name()
        db.session.add(journey)

    db.session.commit()







