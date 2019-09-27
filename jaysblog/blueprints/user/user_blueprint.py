# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 @Time    : 2019/9/24 17:08
 @Author  : Jay Chen
 @FileName: user_blueprint.py
 @GitHub  : https://github.com/cRiii
 @Desc    : 用户蓝图
"""
from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required

from jaysblog import User, db
from jaysblog.utils.response_code import RET

user_bp = Blueprint('user_blueprint', __name__)


@user_bp.route('/editUser', methods=['POST'])
@login_required
def edit_user():
    json_data = request.json
    user_id = json_data['user_id']

    if not all([user_id]):
        return jsonify(code=RET.PARAMS_MISSING_ERROR, msg='参数缺失错误')

    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DATABASE_SELECT_ERROR, msg='查询数据库数据失败')

    if user is None:
        return jsonify(code=RET.USER_NOT_EXIST, msg='修改的用户不存在')

    user.nick_name = json_data['nick_name']
    user.email = json_data['email']
    user.mobile = json_data['mobile']
    user.gender = json_data['gender']
    user.desc = json_data['desc']
    # user.avatar_url = json_data['avatar_url']
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(code=RET.DATABASE_COMMIT_ERROR, msg='修改用户信息失败')

    return jsonify(code=RET.OK, msg='修改用户信息成功')


@user_bp.route('/authPassword', methods=['POST'])
@login_required
def auth_password():
    json_data = request.json
    user_id = json_data['user_id']
    password = json_data['password']

    if not all([user_id, password]):
        return jsonify(code=RET.PARAMS_MISSING_ERROR, msg='参数缺失错误')

    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DATABASE_SELECT_ERROR, msg='查询数据库数据失败')

    if user.check_password(password) is False:
        return jsonify(code=RET.USER_PASSWORD_ERROR, msg='密码输入错误')

    return jsonify(code=RET.OK, msg='密码输入正确')


@user_bp.route('/editPassword', methods=['POST'])
@login_required
def edit_password():
    json_data = request.json
    user_id = json_data['user_id']
    password = json_data['password']
    new_password = json_data['new_password']

    if not all([user_id, password, new_password]):
        return jsonify(code=RET.PARAMS_MISSING_ERROR, msg='参数缺失错误')

    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DATABASE_SELECT_ERROR, msg='查询数据库数据失败')

    if user is None:
        return jsonify(code=RET.USER_NOT_EXIST, msg='用户不存在')

    if user.check_password(password) is False:
        return jsonify(code=RET.USER_PASSWORD_ERROR, msg='密码输入错误')

    user.password = new_password
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(code=RET.DATABASE_COMMIT_ERROR, msg='修改密码错误')

    return jsonify(code=RET.OK, msg='修改密码成功,请重新登陆')




