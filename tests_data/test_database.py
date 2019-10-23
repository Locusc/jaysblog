# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 @Time    : 2019/9/24 10:47
 @Author  : Jay Chen
 @FileName: test_database.py
 @GitHub  : https://github.com/cRiii
 @Desc    : 数据库测试文件
"""
import random
import unittest

from flask import json

from jaysblog import Category, User, db, Post, Comment, constants, Reply
from jaysblog.models import Journey
from jaysblog.utils.tools import random_mobile
from tests_data.base import BaseTestCase


class DataBaseTestCase(BaseTestCase):
    def setUp(self):
        super(DataBaseTestCase, self).setUp()

    def test_print(self):
        self.setUp()
        user_id = db.session.query(User.id).all()
        user_ids = User.query.with_entities(User.id).all()
        user_count = User.query.count()
        admin_user_id = User.query.get(1).id
        print(user_ids)
        print(user_id)
        print('============USER COUNT=============== %s' % user_count)
        print('============USER COUNT=============== %s' % admin_user_id)

    def test_username(self):
        self.setUp()
        user_name_list = User.query.with_entities(User.nick_name).all()
        for i in range(10):
            print(random.choice(user_name_list)[0])

    def test_gender(self):
        self.setUp()
        gender = ('MAN', 'WOMAN')
        genders = ['MAN', 'WOMAN']
        print('============USER GENDER=============== %s' % random.choice(gender))
        print('============USER GENDERS=============== %s' % random.choice(genders))

    def test_random_mobile(self):
        self.setUp()
        for i in range(10):
            print('============RANDOM MOBILE IS=============== %s' % random_mobile())
        print(User.query.filter_by(nick_name='JayChen').first().id)

    def test_paginate(self):
        self.setUp()
        category_id = 1
        paginate = Post.query.filter(Post.post_status == 1, Post.post_category_id == category_id if category_id else True).order_by(
            Post.create_time.asc()).paginate(1, 10, False)
        print(paginate.items)

    def test_post_details(self):
        self.setUp()
        comment = Comment.query.filter_by(comment_status=1, comment_post_id=1).order_by(
            Comment.create_time.desc()).paginate(
            constants.DEFAULT_CURRENT_PAGE_NUM, constants.PAGE_MAX_COMMENT_MESSAGES, False)
        comment_collection = []
        for item in comment.items:
            replies = Reply.query.filter_by(reply_comment_id=item.to_dict()['id']).all()
            if replies is not []:
                for reply in replies:
                    print(reply.to_dict())
                    item.to_dict()['comment_replies_collection'].append(reply.to_dict())
            comment_collection.append(item.to_dict())

        print(comment_collection)

    def test_journey(self):
        self.setUp()
        # journey_list = Journey.query.order_by(Journey.journey_time.asc()).all()
        # collection = []
        # for data in journey_list:
        #     collection.append(data.to_dict())
        # print(collection)

        comment = Comment.query.filter_by(comment_status=1, comment_post_id=1).order_by(
            Comment.create_time.desc()).paginate(
            constants.DEFAULT_CURRENT_PAGE_NUM, constants.PAGE_MAX_COMMENT_MESSAGES, False)
        collection = []
        for item in comment.items:
            collection.append(item.to_dict())
        print(len(collection))