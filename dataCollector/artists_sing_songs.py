#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-09-01 16:23:14
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$

from pymongo import MongoClient
from data_poster import get_artist_index_page
from itertools import ifilter

mongo = MongoClient()
db = mongo['userDig']
song_col = db['songs']
artist_col = db['artists']


def gen_all_songs():
    songs = song_col.find({}, {'_id': 0}, no_cursor_timeout=True)
    for song in songs:
        yield song
    songs.close()


def is_artist_not_exist(artistId):
    return artist_col.find_one({'artistId': artistId}) is None


def get_artist_info(artistId):
    artist_data = get_artist_index_page(artistId)
    return artist_data


def save_artist_data():
    all_songs = gen_all_songs()
    for song in all_songs:
        artists_list = song.setdefault('artists', [])
        artists_list = ifilter(None, artists_list)
        artists_list = ifilter(is_artist_not_exist, artists_list)
        for artistId in artists_list:
            artist_data = get_artist_info(artistId)
            if artist_data:
                try:
                    artist_col.insert_one(artist_data)
                except Exception as e:
                    print(str(e))
                else:
                    print('artist:{} data inserted'.format(artistId))


if __name__ == '__main__':
    save_artist_data()
