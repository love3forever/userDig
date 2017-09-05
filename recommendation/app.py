#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-09-05 15:53:24
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$

from flask import Flask

app = Flask(__name__)


@app.route('/')
def index_page():
    return 'recommendation'


if __name__ == '__main__':
    app.run(debug=True, port=6666, host='0.0.0.0')
