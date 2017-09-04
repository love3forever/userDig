#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-08-31 14:11:10
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$

from pymongo import MongoClient
from neo4j.v1 import GraphDatabase, ConstraintError
from datetime import datetime
from multiprocessing.dummy import Pool

mongo = MongoClient()
db = mongo['userDig']
col = db['playlists']
user_col = db['user_fans_and_follows']
song_col = db['songs']

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "abc@123"))

pool = Pool()


def gen_playlists():
    playlists = col.find({}, {'_id': 0}, no_cursor_timeout=True)
    for playlist in playlists:
        yield playlist
    playlists.close()


def gen_songs_in_playlist():
    playlists = col.find({}, {'_id': 0, 'songs': 1}, no_cursor_timeout=True)
    for playlist in playlists:
        for song in playlist.setdefault('songs', []):
            yield song
    playlists.close()


def gen_all_songs():
    songs = song_col.find({}, {'_id': 0}, no_cursor_timeout=True)
    for song in songs:
        yield song
    songs.close()

def gen_users_relate2_playlist():
    users = user_col.find({'playlist': {'$ne': None}}, {
                          '_id': 0, 'userId': 1, 'playlist': 1}, no_cursor_timeout=True)
    for user in users:
        yield user
    users.close()

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


def save_song_data():
    songs = gen_songs_in_playlist()
    for song in songs:
        try:
            song_col.insert_one(song)
        except Exception as e:
            print(str(e))


def create_song_records(song):
    try:
        with driver.session() as session:
            with session.begin_transaction() as tx:
                tx.run("CREATE ("
                       "song:Song_Music163"
                       "{"
                       "    id:{songId},"
                       "    name:{name},"
                       "    artists:{artists}"
                       "})",
                       songId=song.setdefault('songId', ''),
                       name=song.setdefault('name', ''),
                       artists=song.setdefault('artists', []),
                       )
    except ConstraintError:
        pass
    else:
        print(
            'record:song-{} \
            inserted'.format(song.setdefault('songId', '')))


def create_relation_playlist_and_song(playlist):
    songs = playlist.setdefault('songs', [])
    try:
        with driver.session() as session:
            with session.begin_transaction() as tx:
                for song in songs:
                    tx.run("MATCH (playlist:Playlist_Music163)"
                           "WHERE playlist.id = {playlistId} "
                           "MATCH (song:Song_Music163)"
                           "WHERE song.id = {songId} "
                           "CREATE (playlist)-[:contain]->(song)",
                           songId=song.setdefault('songId', ''),
                           playlistId=playlist.setdefault(
                               'playlistId', '')
                           )
    except Exception as e:
        raise e


if __name__ == '__main__':
    # 创建歌单record
    # playlists = gen_playlists()
    # for playlist in playlists:
    #     create_playlist_record(playlist)
    # 创建用户和歌单关系
    # users = gen_users_relate2_playlist()
    # map.pool(create_relation_user_and_playlist, users)
    # 保存歌曲信息
    # save_song_data()
    # 建立歌曲record
    all_songs = gen_all_songs()
    pool.map(create_song_records, all_songs)
    # 建立歌单和歌曲的关系
    # playlists = gen_playlists()
    # pool.map(create_relation_playlist_and_song, playlists)
