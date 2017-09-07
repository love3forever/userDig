#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-09-05 15:53:24
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$
from datetime import timedelta
from flask import Flask
from flask_jwt import JWT
from userManage.user_model import User
from userManage.user_things import bp_user

app = Flask(__name__)
# 如果使用jwt 必须指明app.config.SECRET_KEY或者JWT_SECRET_KEY
# app.config['SECRET_KEY'] = 'super-secret'
app.register_blueprint(bp_user)


# jwt相关
jwt_config = {
    'JWT_SECRET_KEY': 'jwt_secret',
    'JWT_AUTH_URL_RULE': '/api/v1/auth',
    'JWT_EXPIRATION_DELTA': timedelta(seconds=60)
}

app.config.update(jwt_config)


def authenticate(username, password):
    user = User(username, password)
    flag, _ = user.user_password_check()
    if flag:
        return user
    else:
        return None


def identity(payload):
    print(payload)
    if payload:
        user_id = payload['identity']
        # 返回值为之后的current_identity
        return User.get_user_by_id(user_id)
    else:
        return None


jwt = JWT(app, authenticate, identity)


@jwt.jwt_error_handler
def jwt_error_handler(e):
    return "Something bad happened", 400


if __name__ == '__main__':
    app.run(debug=True, port=12345, host='0.0.0.0')
