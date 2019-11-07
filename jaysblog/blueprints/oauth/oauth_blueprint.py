"""
# @Time     : 2019/10/30 14:18
# @Author   : jay
# @File     : oauth_blueprint.py
# @GitHub   : https://github.com/Locusc
"""
import os
import time
from datetime import datetime

import requests
from flask import Blueprint, jsonify, json, current_app
from flask_login import current_user, login_user

from jaysblog import User, db
from jaysblog.utils.response_code import RET

oauth_bp = Blueprint('oauth_blueprint', __name__)

name = 'github',
consumer_key = os.getenv('GITHUB_CLIENT_ID'),
consumer_secret = os.getenv('GITHUB_CLIENT_SECRET'),
request_token_params = {'scope': 'user'},
base_url = 'https://api.github.com/',
request_token_url = None,
access_token_method = 'POST',
access_token_url = 'https://github.com/login/oauth/access_token',
authorize_url = 'https://github.com/login/oauth/authorize',
user_url = 'https://api.github.com/user',


@oauth_bp.route('/login/<code>')
def oauth_login(code):
    if code is None:
        return jsonify(code=RET.PARAMS_MISSING_ERROR, msg='参数错误或缺失')

    if current_user.is_authenticated:
        if current_user.is_admin is True:
            currentAuthority = 'admin'
        else:
            currentAuthority = 'user'
        return jsonify(code=RET.OK, msg='当前用户已通过认证', currentAuthority=currentAuthority, type='account',
                       user_id=current_user.id)

    return oauth_callback(code)


def oauth_callback(code):
    if code is None:
        return jsonify(code=RET.PARAMS_MISSING_ERROR, msg='参数错误或缺失')

    data = {
        'client_id': consumer_key,
        'client_secret': consumer_secret,
        'code': code,
    }

    access_token_params = requests.post(url=access_token_url[0], data=data)
    if access_token_params.status_code == 200:
        text = access_token_params.text
        if 'access_token' and 'scope' in text:
            args = text.split('&')[0]
            access_token = args.split('=')[1]
            return get_oauth_user_messages(access_token)
        else:
            return jsonify(code=RET.USER_OAUTH_ERROR, msg='第三方认证信息过期,请稍后再试')
    else:
        return jsonify(code=RET.USER_OAUTH_ERROR, msg='获取第三方认证信息错误,请稍后再试')


def get_oauth_user_messages(access_token):
    if access_token is None:
        return jsonify(code=RET.PARAMS_MISSING_ERROR, msg='参数错误或缺失')

    params = {
        'access_token': access_token
    }

    user_messages = requests.get(user_url[0], params)
    user_text = user_messages.text
    user_json = json.loads(user_text)
    try:
        user = User.query.filter(User.id == user_json['id']).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DATABASE_SELECT_ERROR, msg='查询数据库数据错误')

    if user:
        login_user(user, remember=True)
        if user.nick_name != user_json['login']:
            user.nick_name = user_json['login']
            user.email = user_json['email'] if user_json['email'] else user_json['html_url']
        user.last_login_time = datetime.utcnow()
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return jsonify(code=RET.DATABASE_COMMIT_ERROR, msg='提交用户信息到数据库失败')
    else:
        user = User()
        try:
            user_check = User.query.filter_by(nick_name=user_json['login']).first()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(code=RET.DATABASE_COMMIT_ERROR, msg='查询数据库数据错误')
        if user_check:
            user.nick_name = user_json['login'] + str(time.time()).split('.')[1]
        else:
            user.nick_name = user_json['login']
        user.id = user_json['id']
        user.email = user_json['email'] if user_json['email'] else user_json['html_url']
        user.avatar_url = user_json['avatar_url']
        user.nick_name = user_json['login']
        user.password = user_json['login']
        user.desc = user_json['bio']
        user.location = user_json['location']
        user.last_login_time = datetime.utcnow()

        try:
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return jsonify(code=RET.DATABASE_COMMIT_ERROR, msg='提交用户信息到数据库失败')

    return jsonify(code=RET.OK, msg='第三方授权登陆成功')
