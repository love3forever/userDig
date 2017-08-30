#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-08-30 11:37:43
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$
import json

from pymongo import MongoClient
from data_poster import get_user_playlist, get_playlist_detail
from itertools import chain
from datetime import datetime

mongo = MongoClient()
db = mongo['userDig']
col = db['playlists']
user_extral_col = db['user_extral']
user_col = db['user_fans_and_follows']


def gen_allusers():
    all_users = user_col.find({}, {'_id': 0, 'userId': 1})
    for user in all_users:
        yield user


def filter_tracks(track):
    if track:
        track_info = {}
        track_info['songId'] = track.setdefault('id', '')
        track_info['name'] = track.setdefault('name', '')
        track_info['artists'] = [atrist['id'] for atrist in track['artists']]
        return track_info
    else:
        return None


def insert_playlist_data(info):
    if is_playlist_not_exists(info.setdefault('id', '')):
        insert_data = {}
        insert_data['playlistId'] = info.setdefault('id', '')
        insert_data['name'] = info.setdefault('name', '')
        insert_data['tags'] = info.setdefault('tags', [])
        creator = info.setdefault('creator', None)
        if creator:
            insert_data['creator'] = creator.setdefault('userId', '')
        creatTimestamp = info.setdefault('createTime', 0)
        creatTime = datetime.fromtimestamp(int(str(creatTimestamp)[:-3]))
        insert_data['createTime'] = creatTime
        tracks = info.setdefault('tracks', [])
        insert_data['songs'] = map(filter_tracks, tracks)
        insert_data['playCount'] = info.setdefault('playCount', 0)
        insert_data['shareCount'] = info.setdefault('shareCount', 0)
        col.insert_one(insert_data)


def is_playlist_not_exists(playlistId):
    return col.find_one({'playlistId': playlistId}) is None


def crawler_go():
    all_users = gen_allusers()
    for user in all_users:
        print(user['userId'])
        user_playlist_data, _ = get_user_playlist(user['userId'])
        if user_playlist_data:
            # 获取用户收藏的歌单和自己创建的歌单
            theirs_playlist = user_playlist_data['other']
            own_playlist = user_playlist_data['own']
            # 将歌单信息更新至用户数据
            for theirs in theirs_playlist:
                theirs.setdefault('score', 2)
            for own in own_playlist:
                own.setdefault('score', 4)
            all_playlist = theirs_playlist + own_playlist
            user_col.update({'userId': user['userId']}, {
                            '$set': {'playlist': all_playlist}})
            # 获取歌单详情
            for playlist in all_playlist:
                if is_playlist_not_exists(playlist['playlistId']):
                    playlist_data = get_playlist_detail(playlist['playlistId'])
                    if playlist_data:
                        insert_playlist_data(
                            playlist_data.setdefault('result', None))


if __name__ == '__main__':
    crawler_go()
