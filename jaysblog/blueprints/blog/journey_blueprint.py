# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 @Time    : 2019/10/11 15:49
 @Author  : Jay Chen
 @FileName: journey_blueprint.py.py
 @GitHub  : https://github.com/cRiii
 @Desc    : 历程蓝图
"""
from flask import Blueprint, current_app, jsonify

from jaysblog.models import Journey
from jaysblog.utils.response_code import RET

journey_bp = Blueprint('journey_blueprint', __name__)


@journey_bp.route('/list')
def get_journey_list():
    try:
        journey_list = Journey.query.order_by(Journey.journey_time.asc()).all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DATABASE_SELECT_ERROR, msg='查询数据库数据错误')

    collection = []
    for data in journey_list:
        collection.append(data.to_dict())

    data = {
        'list': collection
    }
    return jsonify(code=RET.OK, msg='查询历程列表成功', data=data)
