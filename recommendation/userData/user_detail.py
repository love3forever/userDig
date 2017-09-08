#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-09-08 11:36:51
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$
from flask import make_response, jsonify
from flask.blueprints import Blueprint
from flask_restful import Api, Resource, abort
from flask_jwt import jwt_required, current_identity

from . import user_col

bp_user_detail = Blueprint(__name__, 'bp_user_detail',
                           url_prefix='/api/v1/user')
api_user_detail = Api(bp_user_detail)


@api_user_detail.resource('/userdetail')
class UserDetail(Resource):
    """用户基本信息"""
    @jwt_required()
    def get(self):
        current_user = current_identity
        user_detial = user_col.find_one(
            {'name': current_user.username}, {'_id': 0})
        if user_detial:
            return make_response(jsonify(user_detial))
        else:
            abort(404)
