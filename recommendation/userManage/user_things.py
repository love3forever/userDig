#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-09-07 11:01:41
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$
from flask import jsonify, make_response, current_app
from flask.blueprints import Blueprint
from flask_restful import Api, Resource, request, abort

from user_model import User

bp_user = Blueprint(__name__, 'bp_user', url_prefix='/api/v1/user')
bp_api = Api(bp_user)


@bp_api.resource('/register', methods=['POST'])
class UserRigister(Resource):
    """用户注册"""

    def post(self):
        register_data = request.get_json()
        try:
            username = register_data['username']
            password = register_data['password']
        except Exception as e:
            print(str(e))
            abort(503)

        new_user = User(username, password)
        flag, msg = new_user.user_register()
        error_code = 0 if flag else 1
        result = make_response(jsonify({
            'status': flag,
            'msg': msg,
            'error_code': error_code
        }))
        return result


@bp_api.resource('/update_password', methods=['POST'])
class UserPasswordUpdate(Resource):
    """更新用户密码"""

    def post(self):
        update_password_data = request.get_json()
        try:
            username = update_password_data['username']
            old_password = update_password_data['old_password']
            new_password = update_password_data['new_password']
        except Exception as e:
            print(str(e))
            abort(503)
        user = User(username, old_password)
        flag, msg = user.user_update_password(new_password)
        error_code = 0 if flag else 1
        result = make_response(jsonify({
            'msg': msg,
            'error_code': error_code
        }))
        return result
