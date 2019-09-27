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

from jaysblog import User, db, Comment
from jaysblog.utils.response_code import RET

admin_bp = Blueprint('admin_blueprint', __name__)

# 重置用户密码
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


# 锁定,解锁用户
@admin_bp.route('/lockUser/<int:user_id>', methods=['GET', 'POST'])
@login_required
def lock_user(user_id):
    if not all([user_id]):
        return jsonify(code=RET.PARAMS_MISSING_ERROR, msg='参数缺失错误')
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DATABASE_SELECT_ERROR, msg='查询数据库数据错误')

    if user.is_delete == 1:
        user.is_delete = 0
    else:
        user.is_delete = 1

    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(code=RET.DATABASE_COMMIT_ERROR, msg=('%s用户失败' % '锁定' if user.is_delete == 1 else '解锁'))

    return jsonify(code=RET.OK, msg=('%s用户成功' % '锁定' if user.is_delete == 1 else '解锁'))


# 审核留言
@admin_bp.route('/checkComment/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def check_comment(comment_id):
    if not all([comment_id]):
        return jsonify(code=RET.PARAMS_MISSING_ERROR, msg='参数缺失错误')
    try:
        comment = Comment.query.get(comment_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DATABASE_SELECT_ERROR, msg='查询数据库数据失败')




