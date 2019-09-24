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

from jaysblog import Category, User, db
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