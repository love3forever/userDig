#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-09-08 11:36:38
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$
from pymongo import MongoClient
mongo = MongoClient()
db = mongo['userDig']
user_col = db['user_fans_and_follows']
song_col = db['songs']
playlist_col = db['playlists']
artist_col = db['artists']
