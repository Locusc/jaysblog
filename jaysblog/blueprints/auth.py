# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 @Time    : 2019/9/17 17:51
 @Author  : Jay Chen
 @FileName: auth.py
 @GitHub  : https://github.com/cRiii
"""

from flask import Blueprint

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    1/0
    return '<h1>登陆的接口</h1>'
