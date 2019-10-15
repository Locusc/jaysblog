# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 @Time    : 2019/9/17 17:51
 @Author  : Jay Chen
 @FileName: auth.py
 @GitHub  : https://github.com/cRiii
"""
from datetime import datetime

from flask import Blueprint, make_response, request, current_app, jsonify
from flask_login import current_user, login_user, logout_user, login_required

from jaysblog import constants, User, db
from jaysblog.utils.captcha import captcha
from jaysblog.extensions import redis_store
from jaysblog.utils.response_code import RET

auth_bp = Blueprint('auth_blueprint', __name__)


@auth_bp.route("/image_code")
def get_image_code():
    """获取图片验证码"""
    # 获取当前图片的UUID编号  前端以时间戳或者唯一的uuid传入
    image_code_id = request.args.get('code_id')
    # 生成验证码
    """
        generate_captcha()  Returns:
            A tuple, (name, text, StringIO.value).
            For example:
                ('fXZJN4AFxHGoU5mIlcsdOypa', 'JGW9', '\x89PNG\r\n\x1a\n\x00\x00\x00\r...')
    """
    name, text, image = captcha.captcha.generate_captcha()
    try:
        # 保存获取的验证码到redis当中
        redis_store.set('ImageCodeId_%s' % image_code_id, text, constants.IMAGE_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return make_response(jsonify(code=RET.REDIS_SAVE_ERROR, msg='保存图片验证码信息到redis服务器失败'))

    response = make_response(image)
    # 设置content-type 请求返回body数据类型
    response.headers["Content-Type"] = "image/jpeg"
    # 返回验证码图片到前端
    return response


@auth_bp.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin is True:
            currentAuthority = 'admin'
        else:
            currentAuthority = 'user'
        return jsonify(code=RET.OK, msg='当前用户已通过认证', currentAuthority=currentAuthority, type='account')
    json_data = request.json
    nick_name = json_data['userName']
    password = json_data['password']
    remember = json_data['autoLogin']
    image_code = json_data['verificationCode']
    image_code_id = json_data['imageCodeId']

    if not all([nick_name, password, image_code, image_code_id]):
        return jsonify(code=RET.PARAMS_MISSING_ERROR, msg='参数错误,缺少参数')

    redis_image_code = redis_store.get("ImageCodeId_"+str(image_code_id))
    # 判断是否过期
    if not redis_image_code:
        return jsonify(code=RET.IMAGE_CODE_OVERDUE_ERROR, msg="图片验证码已过期")
    # 判断图片验证码是否正确
    if redis_image_code.lower() != bytes(image_code.lower(), encoding='utf-8'):
        return jsonify(code=RET.IMAGE_CODE_INPUT_ERROR, msg="图片验证码输入错误")

    try:
        user = User.query.filter_by(nick_name=nick_name).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DATABASE_SELECT_ERROR, msg='查询数据库用户信息错误')

    if not user:
        return jsonify(code=RET.USER_NOT_EXIST, msg='用户不存在')

    if user.is_delete == 0:
        return jsonify(code=RET.USER_LOCK_ERROR, msg='该用户已被禁止登陆,请联系管理员')

    if user.check_password(password) is False:
        return jsonify(code=RET.USER_PASSWORD_ERROR, msg='密码错误')

    try:
        login_user(user, remember)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.USER_LOGIN_ERROR, msg='用户登陆失败')

    user.last_login_time = datetime.now()

    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(code=RET.DATABASE_COMMIT_ERROR, msg='更新用户登陆时间错误')

    if user.is_admin is True:
        currentAuthority = 'admin'
    else:
        currentAuthority = 'user'

    return jsonify(code=RET.OK, msg='登陆成功', currentAuthority=currentAuthority)


@auth_bp.route('/register', methods=['POST'])
def register():
    json_data = request.json
    nick_name = json_data['username']
    password = json_data['password']
    mobile = json_data['mobile']
    email = json_data['email']
    desc = json_data['desc']
    if not all([nick_name, password, mobile, email, desc]):
        return jsonify(code=RET.PARAMS_MISSING_ERROR, msg='参数缺失错误')

    try:
        user = User.query.filter(User.nick_name == nick_name or
                                 User.mobile == mobile or
                                 User.email == email)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DATABASE_SELECT_ERROR, msg='查询数据库数据错误')
    if user:
        if user.nick_name == nick_name:
            return jsonify(code=RET.USER_REGISTER_ERROR, msg='用户名已存在')
        elif user.mobile == mobile:
            return jsonify(code=RET.USER_REGISTER_ERROR, msg='联系电话已存在')
        elif user.email == email:
            return jsonify(code=RET.USER_REGISTER_ERROR, msg='邮箱已存在')
    else:
        user.desc = desc
        user.email = email
        user.mobile = mobile
        user.password = password
        user.nick_name = nick_name

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(code=RET.DATABASE_COMMIT_ERROR, msg='注册用户信息失败')
    try:
        login_user(user)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.USER_LOGIN_ERROR, msg='用户登陆失败')
    return jsonify(code=RET.OK, msg='用户注册并登陆成功')


@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    try:
        logout_user()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.USER_LOGOUT_ERROR, msg='用户退出失败')
    return jsonify(code=RET.OK, msg='用户已退出')



