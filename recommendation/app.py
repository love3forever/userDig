#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-09-05 15:53:24
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$

from flask import Flask, make_response, jsonify
from flask_jwt import JWT, jwt_required, current_identity
from userManage.user_model import User

from userManage.user_things import bp_user

app = Flask(__name__)
# 如果使用jwt 必须指明app.config.SECRET_KEY或者JWT_SECRET_KEY
app.config['SECRET_KEY'] = 'super-secret'
app.register_blueprint(bp_user)


def authenticate(username, password):
    user = User(username, password)
    if user.user_password_check():
        print(user)
        return user


def identity(payload):
    print(payload)
    user_id = payload['identity']
    print(user_id)
    return User.get_user_by_id(user_id)


jwt = JWT(app, authenticate, identity)


@app.route('/protected', methods=['GET', 'POST'])
@jwt_required()
def protected():
    return make_response(jsonify({"a": 'b'}))


if __name__ == '__main__':
    app.run(debug=True, port=12345, host='0.0.0.0')
