# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 @Time    : 2019/9/24 10:10
 @Author  : Jay Chen
 @FileName: base.py
 @GitHub  : https://github.com/cRiii
 @Desc    : 测试基类
"""
import unittest
from jaysblog import db, create_app, User


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        app = create_app('testing')
        self.context = app.test_request_context()
        self.context.push()
        self.client = app.test_client()
        self.runner = app.test_cli_runner()




