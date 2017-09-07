#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-09-07 09:42:02
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from . import user_col


class User(object):
    """docstring for User"""

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def user_register(self):
        # 用户注册
        if user_col.find_one({'username': self.username}) is not None:
            error_msg = 'username:{} has been used'.format(self.username)
            return False, error_msg
        else:
            user_data = {
                'username': self.username,
                'password': generate_password_hash(self.password)
            }
            user_col.insert_one(user_data)
            success_msg = 'user:{} register successfully'.format(self.username)
            return True, success_msg

    def user_password_check(self):
        user_in_db = user_col.find_one({'username': self.username})
        if user_in_db is not None:
            if check_password_hash(user_in_db['password'], self.password):
                return True, str(user_in_db['_id'])
            else:
                return False, None
        else:
            return False, None

    def user_update_password(self, newpassword):
        flag, _ = self.user_password_check()
        if flag:
            user_col.update_one({'username': self.username}, {
                                '$set': {'password':
                                         generate_password_hash(newpassword)}})
            return True, 'user:{} password updated'.format(self.username)
        else:
            return False, 'password error'

    @staticmethod
    def get_user_by_id(id):
        mongo_id = ObjectId(id)
        print(mongo_id)
        user_data = user_col.find_one({'_id': mongo_id})
        if user_data is not None:
            return User(user_data['username'], user_data['password'])
        else:
            return None

    @property
    def id(self):
        flag, user_id = self.user_password_check()
        if flag:
            return user_id
        else:
            return None
