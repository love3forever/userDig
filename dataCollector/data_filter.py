#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-09-04 15:52:34
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$

from pymongo import MongoClient

mongo = MongoClient()
db = mongo['userDig']
playlist_col = db['playlists']
user_col = db['user_fans_and_follows']


def filter_user_col():
    all_users = user_col.find()
    for user in all_users:
        if user_col.find({'userId': user['userId']}).count() != 1:
            print('removing user:{}'.format(user['userId']))
            user_col.remove(user)


def filter_playlist_col():
    all_playlists = playlist_col.find()
    for playlist in all_playlists:
        if playlist_col.find({'playlistId': playlist['playlistId']}).count() != 1:
            print('removing playlist:{}'.format(playlist['playlistId']))
            playlist_col.remove(playlist)


if __name__ == '__main__':
    filter_user_col()
    filter_playlist_col()
