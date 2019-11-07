# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 @Time    : 2019/9/20 16:46
 @Author  : Jay Chen
 @FileName: blog_controller.py
 @GitHub  : https://github.com/cRiii
"""

from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from jaysblog import constants, Post, Comment, db, Reply, UsersLikePosts
from jaysblog import Category
from jaysblog.utils.response_code import RET

blog_bp = Blueprint('blog_blueprint', __name__)


# 获取分类列表
@blog_bp.route('/category', methods=['GET', 'POST'])
def get_category_list():
    pageSize = request.json.get('pageSize', constants.DEFAULT_CURRENT_PAGE_NUM)
    current = request.json.get('current', constants.PAGE_MAX_CATEGORY_MESSAGES)
    if not all([pageSize, current]):
        return jsonify(code=RET.PARAMS_MISSING_ERROR, msg='参数缺失错误')

    try:
        paginate = Category.query.paginate(current, pageSize, False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DATABASE_SELECT_ERROR, msg='查询数据库数据错误')

    collection = []
    for item in paginate.items:
        collection.append(item.to_dict())
    data = {
        "paginates": {
            "current": paginate.page,
            "pageSize": paginate.per_page,
            "total": paginate.total
        },
        "list": collection
    }
    return jsonify(code=RET.OK, msg='查询分类列表成功', data=data)


# 获取博文列表
@blog_bp.route('/post', methods=['GET', 'POST'])
def get_post_list():
    category_id = request.json.get("category_id")
    pageSize = request.json.get("pageSize", constants.DEFAULT_CURRENT_PAGE_NUM)
    current = request.json.get("current", constants.PAGE_MAX_POST_MESSAGES)

    if not all([pageSize, current]):
        return jsonify(code=RET.PARAMS_MISSING_ERROR, msg='参数缺失错误')

    try:
        paginate = Post.query.filter(Post.post_status == 1,
                                     Post.post_category_id == category_id if category_id else True
                                     ).order_by(Post.create_time.asc()).paginate(current, pageSize, False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DATABASE_SELECT_ERROR, msg='查询数据库数据错误')

    collection = []
    for item in paginate.items:
        collection.append(item.to_dict())

    data = {
        "paginates": {
            "current": paginate.page,
            "pageSize": paginate.per_page,
            "total": paginate.total
        },
        "list": collection
    }
    return jsonify(code=RET.OK, msg='查询文章列表成功', data=data)


# 获取博文详情
@blog_bp.route('/post/details/<int:post_id>', methods=['GET'])
def get_post_details(post_id):
    if not all([post_id]):
        return jsonify(code=RET.PARAMS_MISSING_ERROR, msg='参数缺失错误')

    try:
        post = Post.query.filter_by(id=post_id).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DATABASE_SELECT_ERROR, msg='查询数据库数据失败')

    post.post_clicks = post.post_clicks + 1
    try:
        db.session.commit()
    except Exception as e:
        current_user.logger.error(e)
        return jsonify(code=RET.DATABASE_COMMIT_ERROR, msg='更新点击量失败')

    data = {
        "post": post.to_dict_details(),
    }

    return jsonify(code=RET.OK, msg='查询文章详情成功', data=data)


# 查询文章评论
@blog_bp.route('/post/comments/<int:post_id>', methods=['GET'])
def get_post_comments(post_id):
    if not all([post_id]):
        return jsonify(code=RET.PARAMS_MISSING_ERROR, msg='参数缺失错误')

    try:
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
        "comments": {
            "paginates": {
                "current": comment.page,
                "pageSize": comment.per_page,
                "total": comment.total
            },
            "list": collection
        }
    }

    return jsonify(code=RET.OK, msg='查询文章评论成功', data=data)


# 评论
@blog_bp.route('/put/comment', methods=['POST'])
@login_required
def put_comment():
    json_data = request.json
    comment_content = json_data['commentContent']
    comment_post_id = json_data['commentPostId']

    if not all([comment_content, comment_post_id]):
        return jsonify(code=RET.PARAMS_MISSING_ERROR, msg='参数缺失错误')

    try:
        post = Post.query.filter_by(id=comment_post_id).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DATABASE_SELECT_ERROR, msg='查询数据库数据错误')

    if post:
        comment = Comment()
        comment.comment_content = comment_content
        comment.comment_post_id = comment_post_id
        comment.comment_user_id = current_user.id
        comment.comment_from_admin = 1 if current_user.is_admin else 0
        comment.comment_status = 1
        try:
            db.session.add(comment)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return jsonify(code=RET.DATABASE_COMMIT_ERROR, msg='提交评论失败')
    else:
        return jsonify(code=RET.PARAMS_MISSING_ERROR, msg='当前文章状态错误, 暂不支持评论')

    return jsonify(code=RET.OK, msg='评论成功')


# 回复
@blog_bp.route('/put/reply', methods=['POST'])
@login_required
def put_reply():
    json_data = request.json
    reply_to_user = json_data['toUser']
    reply_content = json_data['content']
    reply_comment_id = json_data['commentId']

    if not all([reply_comment_id, reply_content, reply_to_user]):
        return jsonify(code=RET.PARAMS_MISSING_ERROR, msg='参数缺失错误')

    try:
        comment = Comment.query.filter_by(id=reply_comment_id).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DATABASE_SELECT_ERROR, msg='查询数据库数据错误')

    if comment is None:
        return jsonify(code=RET.PARAMS_MISSING_ERROR, msg='当前评论状态错误, 暂不支持回复')
    else:
        reply = Reply()
        reply.reply_to_user = reply_to_user
        reply.reply_content = reply_content
        reply.reply_from_user = current_user.nick_name
        reply.reply_comment_id = reply_comment_id
        reply.reply_status = 1

        try:
            db.session.add(reply)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return jsonify(code=RET.DATABASE_COMMIT_ERROR, msg='添加回复到数据库失败')

    return jsonify(code=RET.OK, msg='回复成功')


# 点赞
@blog_bp.route('/put/like/<int:post_id>')
@login_required
def put_like_num(post_id):
    print(post_id)
    if not all([post_id]):
        return jsonify(code=RET.PARAMS_MISSING_ERROR, msg='参数缺失错误')

    try:
        post = Post.query.filter_by(id=post_id).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DATABASE_SELECT_ERROR, msg='查询数据库数据错误')

    if post is None:
        return jsonify(code=RET.PARAMS_MISSING_ERROR, msg='当前文章状态错误, 暂不支持点赞')
    else:
        try:
            users_like_posts = UsersLikePosts.query.filter(
                UsersLikePosts.user_id == current_user.id, UsersLikePosts.user_like_post_id == post_id
            ).first()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(code=RET.DATABASE_SELECT_ERROR, msg='查询数据库数据错误')

        if users_like_posts:
            return jsonify(code=RET.DATABASE_COMMIT_ERROR, msg='你点赞过了, 谢谢你的支持')
        else:
            post.post_like_num = post.post_like_num + 1
            ulp = UsersLikePosts()
            ulp.user_id = current_user.id
            ulp.user_like_post_id = post_id

            try:
                db.session.add(ulp)
                db.session.commit()
            except Exception as e:
                current_app.logger.error(e)
                return jsonify(code=RET.DATABASE_COMMIT_ERROR, msg='更新数据错误')

            return jsonify(code=RET.OK, msg='点赞成功')


