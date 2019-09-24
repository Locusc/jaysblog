# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 @Time    : 2019/9/20 16:47
 @Author  : Jay Chen
 @FileName: back_manager_controller.py
 @GitHub  : https://github.com/cRiii
"""

from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required

from jaysblog import User, db
from jaysblog.utils.response_code import RET

admin_bp = Blueprint('admin_blueprint', __name__)


@admin_bp.route('/resetPassword/<int:user_id>', methods=['POST'])
@login_required
def reset_password(user_id):
    if not all([user_id]):
        return jsonify(code=RET.PARAMS_MISSING_ERROR, msg='参数缺失错误')

    user = User.query.get(user_id)
    if user is None:
        return jsonify(code=RET.USER_NOT_EXIST, msg='重置密码错误,当前ID的用户不存在')

    user.password = '123456'
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(code=RET.DATABASE_COMMIT_ERROR, msg='重置密码失败')

    return jsonify(code=RET.OK, msg='重置密码成功, 请重新登陆')



