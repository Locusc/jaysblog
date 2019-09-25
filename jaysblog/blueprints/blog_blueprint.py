# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 @Time    : 2019/9/20 16:46
 @Author  : Jay Chen
 @FileName: blog_controller.py
 @GitHub  : https://github.com/cRiii
"""

from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required
from jaysblog import constants, Post, Comment
from jaysblog import Category
from jaysblog.utils.response_code import RET

blog_bp = Blueprint('blog_blueprint', __name__)


@blog_bp.route('/category', methods=['GET', 'POST'])
@login_required
def get_category_list():
    page = request.json.get('pageSize', constants.DEFAULT_CURRENT_PAGE_NUM)
    currentPage = request.json.get('currentPage', constants.PAGE_MAX_CATEGORY_MESSAGES)
    if not all([page, currentPage]):
        return jsonify(code=RET.PARAMS_MISSING_ERROR, msg='参数缺失错误')

    try:
        paginate = Category.query.paginate(currentPage, page, False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DATABASE_SELECT_ERROR, msg='查询数据库数据错误')

    collection = []
    for item in paginate.items:
        collection.append(item.to_dict())
    data = {
        "pagination": {
            "current": paginate.page,
            "pageSize": paginate.per_page,
            "total": paginate.total
        },
        "list": collection
    }
    return jsonify(code=RET.OK, msg='查询分类列表成功', data=data)


@blog_bp.route('/post', methods=['GET', 'POST'])
def get_post_list():
    page = request.json.get("pageSize", constants.DEFAULT_CURRENT_PAGE_NUM)
    currentPage = request.json.get("currentPage", constants.PAGE_MAX_POST_MESSAGES)

    if not all([page, currentPage]):
        return jsonify(code=RET.PARAMS_MISSING_ERROR, msg='参数缺失错误')

    try:
        paginate = Post.query.filter_by(post_status=1).order_by(Post.create_time.asc()).paginate(currentPage, page,
                                                                                                 False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DATABASE_SELECT_ERROR, msg='查询数据库数据错误')

    collection = []
    for item in paginate.items:
        collection.append(item.to_dict())

    data = {
        "pagination": {
            "current": paginate.page,
            "pageSize": paginate.per_page,
            "total": paginate.total
        },
        "list": collection
    }

    return jsonify(code=RET.OK, msg='查询文章列表成功', data=data)
