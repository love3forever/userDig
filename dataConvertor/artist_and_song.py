#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-09-04 15:25:33
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$
from pymongo import MongoClient
from neo4j.v1 import GraphDatabase, ConstraintError

mongo = MongoClient()
db = mongo['userDig']
artist_col = db['artists']
song_col = db['songs']

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "abc@123"))


def gen_artist_data():
    all_artist = artist_col.find({}, {'_id': 0, 'artist_alias': 0, 'top50': 0})
    for artist in all_artist:
        yield artist
    all_artist.close()


def creat_artist_and_songs(artistId):
    songs = song_col.find({'artists': {'$in': [artistId]}}, {
                          '_id': 0, 'songId': 1})
    for song in songs:
        try:
            with driver.session() as session:
                with session.begin_transaction() as tx:
                    tx.run("MATCH (song:Song_Music163)"
                           "WHERE song.id = {songId} "
                           "MATCH (artist:Artist_Music163)"
                           "WHERE artist.id = {artistId} "
                           "CREATE (artist)-[:sing]->(song)",
                           songId=song.setdefault('songId', ''),
                           artistId=artistId
                           )
        except Exception as e:
            print(str(e))
        else:
            print('song:{} relationship complete'.format(song['songId']))


def create_artist_records(artist):
    if artist:
        try:
            with driver.session() as session:
                with session.begin_transaction() as tx:
                    tx.run("CREATE ("
                           "artist:Artist_Music163"
                           "{"
                           "    id:{artistId},"
                           "    name:{artist_name}"
                           "})",
                           artistId=artist.setdefault('artistId', ''),
                           artist_name=artist.setdefault('artist_name', '')
                           )
        except ConstraintError:
            print('artist:{} exists already'.format(
                artist.setdefault('artistId', '')))
        else:
            print('artist:{} record inserted'.format(
                artist.setdefault('artistId', '')))


if __name__ == '__main__':
    all_artist = gen_artist_data()
    for artist in all_artist:
        # create_artist_records(artist)
        creat_artist_and_songs(artist['artistId'])
