#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-09-07 09:41:49
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$

from pymongo import MongoClient

user_mongo = MongoClient()
user_db = user_mongo['userDig']
user_col = user_db['user']
