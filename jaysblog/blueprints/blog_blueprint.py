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
@login_required
def get_post_list():
    category_id = request.json.get("category_id")
    page = request.json.get("pageSize", constants.DEFAULT_CURRENT_PAGE_NUM)
    currentPage = request.json.get("currentPage", constants.PAGE_MAX_POST_MESSAGES)

    if not all([page, currentPage]):
        return jsonify(code=RET.PARAMS_MISSING_ERROR, msg='参数缺失错误')

    try:
        paginate = Post.query.filter(Post.post_status == 1,
                                     Post.post_category_id == category_id if category_id else True
                                     ).order_by(Post.create_time.asc()).paginate(1, 10, False)
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


@blog_bp.route('/post/details/<int:post_id>', methods=['GET'])
@login_required
def get_post_details(post_id):

    if not all([post_id]):
        return jsonify(code=RET.PARAMS_MISSING_ERROR, msg='参数缺失错误')

    try:
        post = Post.query.filter_by(id=post_id).first()
        comment = Comment.query.filter_by(comment_status=1, comment_post_id=post_id).order_by(
            Comment.create_time.desc()).paginate(
            constants.DEFAULT_CURRENT_PAGE_NUM, constants.PAGE_MAX_COMMENT_MESSAGES, False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DATABASE_SELECT_ERROR, msg='查询数据库数据失败')

    collection = []
    for item in comment.items:
        collection.append(item.to_dict())

    data = {
        "post": post.to_dict_details(),
        "comments": {
            "pagination": {
                "current": comment.page,
                "pageSize": comment.per_page,
                "total": comment.total
            },
            "list": collection
        }
    }

    return jsonify(code=RET.OK, msg='查询文章详情成功', data=data)





