#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-09-07 10:57:08
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$
from flask import jsonify
from app import app


client = app.test_client()

with client as c:
    c.post('http://localhost:12345/auth', jsonify({
        "username": "wangmeng",
        "password": "abc@123"
    }))
