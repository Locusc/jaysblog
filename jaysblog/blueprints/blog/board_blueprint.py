"""
# @Time     : 2019/10/28 10:54
# @Author   : jay
# @File     : board_blueprint.py
# @GitHub   : https://github.com/cRiii
"""

from flask import Blueprint, request, jsonify, current_app

from jaysblog import constants, db
from jaysblog.models import MessageBoard
from jaysblog.utils.response_code import RET

board_bp = Blueprint('board_blueprint', __name__)


@board_bp.route('/list', methods=['POST'])
def get_board_list():
    pageSize = request.json.get('pageSize', constants.PAGE_MAX_MESSAGE_BOARD)
    current = request.json.get('current', constants.DEFAULT_CURRENT_PAGE_NUM)

    if not all([pageSize, current]):
        return jsonify(code=RET.PARAMS_MISSING_ERROR, msg='参数缺失错误')

    try:
        paginate = MessageBoard.query.order_by(MessageBoard.create_time.desc()).filter_by(board_status=1)\
            .paginate(current, pageSize, False)
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

    return jsonify(code=RET.OK, msg='查询留言列表成功', data=data)


@board_bp.route('/addBoardMessage', methods=['POST'])
def add_board_message():
    board_user = request.json.get('nickName')
    board_desc = request.json.get('desc')
    board_email = request.json.get('email')

    if not all([board_email, board_user, board_desc]):
        return jsonify(code=RET.PARAMS_MISSING_ERROR, msg='参数缺失错误')

    board = MessageBoard()
    board.board_user = board_user
    board.board_desc = board_desc
    board.board_email = board_email
    board.board_status = 1

    try:
        db.session.add(board)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(code=RET.DATABASE_COMMIT_ERROR, msg='添加留言到数据库失败')

    return jsonify(code=RET.OK, msg='添加留言成功, 管理员会尽快回复您')
