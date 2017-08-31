#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-08-31 14:11:10
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$

from pymongo import MongoClient
from neo4j.v1 import GraphDatabase, ConstraintError
from datetime import datetime

mongo = MongoClient()
db = mongo['userDig']
col = db['playlists']
user_col = db['user_fans_and_follows']

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "abc@123"))


def gen_playlists():
    playlists = col.find({}, {'_id': 0, 'songs': 0})
    for playlist in playlists:
        yield playlist


def gen_users_relate2_playlist():
    users = user_col.find({'playlist': {'$ne': None}}, {
                          '_id': 0, 'userId': 1, 'playlist': 1})
    for user in users:
        yield user


def create_playlist_record(playlist):
    if playlist:
        try:
            with driver.session() as session:
                with session.begin_transaction() as tx:
                    tx.run("CREATE ("
                           "playlist:Playlist_Music163"
                           "{"
                           "    id:{playlistId},"
                           "    name:{name},"
                           "    creatorId:{creator},"
                           "    shareCount:{shareCount},"
                           "    playCount:{playCount},"
                           "    tags:{tags},"
                           "    createTime:{createTime}"
                           "})",
                           playlistId=playlist.setdefault('playlistId', ''),
                           name=playlist.setdefault('name', ''),
                           creator=playlist.setdefault('creator', ''),
                           shareCount=playlist.setdefault('shareCount', 0),
                           playCount=playlist.setdefault('playCount', 0),
                           tags=playlist.setdefault('tags', []),
                           createTime=playlist.setdefault(
                               'createTime', datetime.now()).strftime(
                               '%Y-%m-%d %H:%M:%S')
                           )
        except ConstraintError:
            pass
        else:
            print(
                'record:playlist-{} \
                inserted'.format(playlist.setdefault('playlistId', '')))


def create_relation_user_and_playlist(user):
    if user:
        all_playlists = user.setdefault('playlist', [])
        userId = user.setdefault('userId', '')
        try:
            with driver.session() as session:
                with session.begin_transaction() as tx:
                    for playlist in all_playlists:
                        if playlist['score'] == 4:
                            tx.run("MATCH (user:User_Music163)"
                                   "WHERE user.name = {userId} "
                                   "MATCH (playlist:Playlist_Music163)"
                                   "WHERE playlist.id = {playlistId} "
                                   "CREATE (user)-[:create]->(playlist)",
                                   userId=userId,
                                   playlistId=playlist.setdefault(
                                       'playlistId', '')
                                   )
                        else:
                            tx.run("MATCH (user:User_Music163)"
                                   "WHERE user.name = {userId} "
                                   "MATCH (playlist:Playlist_Music163)"
                                   "WHERE playlist.id = {playlistId} "
                                   "CREATE (user)-[:like]->(playlist)",
                                   userId=userId,
                                   playlistId=playlist.setdefault(
                                       'playlistId', '')
                                   )
        except Exception as e:
            raise e
        else:
            print('user:{} and playlist relationship complete'.format(userId))


if __name__ == '__main__':
    # playlists = gen_playlists()
    # for playlist in playlists:
    #     create_playlist_record(playlist)
    users = gen_users_relate2_playlist()
    for user in users:
        create_relation_user_and_playlist(user)
