#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-08-29 11:03:27
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$

from neo4j.v1 import GraphDatabase, ConstraintError
from pymongo import MongoClient

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "abc@123"))

mongo = MongoClient()
db = mongo['userDig']
col = db['user_fans_and_follows']


def gen_userdata_from_mongo():
    all_users = col.find(
        {}, {'_id': 0, 'userId': 1, 'fans_list': 1,
             'follows_list': 1, 'name': 1, 'location': 1,
             'gender': 1})
    for user in all_users:
        yield user


def create_user_in_noe4j(user):
    if user:
        try:
            with driver.session() as session:
                with session.begin_transaction() as tx:
                    tx.run("CREATE ("
                           "user:User_Music163"
                           "{"
                           "    name:{userid},"
                           "    username:{username},"
                           "    location:{location},"
                           "    gender:{gender}"
                           "})",
                           userid=user.setdefault('userId', ''),
                           username=user.setdefault('name', ''),
                           location=user.setdefault('location', 'unknown'),
                           gender=user.setdefault('gender', 'unknown')
                           )
        except ConstraintError:
            print('user:{} exists already'.format(
                user.setdefault('userId', '')))
        else:
            print('user:{} record inserted'.format(
                user.setdefault('userId', '')))


def create_relations_in_neo4j(user):
    if user:
        userId = user.setdefault('userId', '')
        follows_list = user.setdefault('follows_list', [])
        followed_list = user.setdefault('fans_list', [])
        try:
            with driver.session() as session:
                with session.begin_transaction() as tx:
                    for fanId in followed_list:
                        tx.run("MATCH (user:User_Music163)"
                               "WHERE user.name = {userId} "
                               "MATCH (fan:User_Music163)"
                               "WHERE fan.name = {fanId} "
                               "CREATE (user)-[:followed]->(fan)",
                               userId=userId,
                               fanId=fanId
                               )
                    for followsId in follows_list:
                        tx.run("MATCH (user:User_Music163)"
                               "WHERE user.name = {userId} "
                               "MATCH (follows:User_Music163)"
                               "WHERE follows.name = {followsId} "
                               "CREATE (user)-[:follows]->(follows)",
                               userId=userId,
                               followsId=followsId
                               )
        except Exception as e:
            raise e
        else:
            print('user:{} relationship complete'.format(userId))


if __name__ == '__main__':
    for user in gen_userdata_from_mongo():
        create_user_in_noe4j(user)

    for user in gen_userdata_from_mongo():
        create_relations_in_neo4j(user)
