#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-08-23 14:43:56
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$
from pymongo import MongoClient, DESCENDING
from itertools import chain, islice
import data_poster
from multiprocessing.dummy import Pool

mongo = MongoClient()
db = mongo['userDig']
col = db['user_fans_and_follows']
pool = Pool()

seed_userId = '77159064'


def get_user_info(userId):
    user_info = dict()
    user_info.setdefault('userId', userId)
    user_basic_info = data_poster.get_user_index(userId)
    if user_basic_info:
        user_info.update(user_basic_info)
        if int(user_info['fans']) < 300:
            user_fans_list = data_poster.get_user_fans(userId)
            for fans in user_fans_list:
                user_info.setdefault('fans_list', []).extend(
                    [x['userId'] for x in fans])
        else:
            for x in range(1, 11):
                user_fans_withoffset = data_poster.get_user_fans_withoffset(
                    userId, x)
                if user_fans_withoffset:
                    user_info.setdefault('fans_list', []).extend(
                        [x['userId'] for x in user_fans_withoffset])
                else:
                    break
        if int(user_info['follows']) < 300:
            user_follows_list = data_poster.get_user_follows(userId)
            for follows in user_follows_list:
                user_info.setdefault('follows_list', []).extend(
                    [x['userId'] for x in follows])
        else:
            for x in range(1, 11):
                user_follows_withoffset = \
                    data_poster.get_user_follows_withoffset(userId, x)
                if user_follows_withoffset:
                    user_info.setdefault('follows_list', []).extend(
                        [x['userId'] for x in user_follows_withoffset])
                else:
                    break
    return user_info


def crawler_gogo(times_end=10):
    if times_end:
        max_iteration_times = col.find().sort(
            'iteration_times', DESCENDING).limit(1)
        if max_iteration_times.count() != 0 and \
                max_iteration_times[0]['iteration_times'] > times_end:
            return
        max_times = 0
        if max_iteration_times.count() != 0:
            max_times = max_iteration_times[0]['iteration_times']
        for i in range(max_times, times_end + 1):
            print('function run at {} times iteration'.format(i))
            if i == 0:
                user_info = get_user_info(seed_userId)
                insert_data(user_info, i)
            else:
                last_interation = col.find(
                    {'iteration_times': i - 1},
                    {'_id': 0, 'fans_list': 1, 'follows_list': 1})
                for item in last_interation:
                    fans_list = item.setdefault('fans_list', [])
                    follows_list = item.setdefault('follows_list', [])
                    all_list = chain(fans_list, follows_list)
                    all_list_available = filter(is_user_not_exists, all_list)
                    thread_num = len(all_list_available) / 100
                    for num in range(thread_num):
                        partial_list_available = islice(
                            all_list_available, num * 100, num * 100 + 100)
                        user_data = pool.imap(
                            get_user_info, partial_list_available)
                        insert_func = wrap_insert_data(i)
                        pool.map(insert_func, user_data)


def is_user_not_exists(userId):
    data = col.find_one({'userId': userId})
    return data is None


def wrap_insert_data(times):
    iteration_times = times

    def save_data(info):
        insert_data = dict(info)
        if info and is_user_not_exists(insert_data['userId']):
            insert_data.setdefault('iteration_times', iteration_times)
            try:
                col.insert_one(insert_data)
            except Exception:
                pass
            else:
                print('user:{} info inserted'.format(insert_data['userId']))
    return save_data


def insert_data(info, iteration_times):
    insert_data = dict(info)
    if info and is_user_not_exists(insert_data['userId']):
        insert_data.setdefault('iteration_times', iteration_times)
        try:
            col.insert_one(insert_data)
        except Exception:
            pass
        else:
            print('user:{} info inserted'.format(insert_data['userId']))


if __name__ == '__main__':
    crawler_gogo(4)
