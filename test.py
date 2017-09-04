#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-08-23 11:57:19
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$

import unittest
from dataCollector import data_poster

wrong_userId = '-1'
my_userId = 77159064


class TestUserInfo(unittest.TestCase):
    """docstring for TestUserInfo"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_user_follows(self):
        user_follows = data_poster.get_user_follows(wrong_userId)
        my_follows = data_poster.get_user_fans(my_userId)
        assert list(user_follows) == [] and list(my_follows) != []

    def test_get_user_follows_withoffset(self):
        user_follows_page_1 = data_poster.get_user_follows_withoffset(
            wrong_userId, 1)
        my_follows_page_1 = data_poster.get_user_follows_withoffset(
            my_userId, 1)
        assert user_follows_page_1 == [] and my_follows_page_1 != []

    def test_get_user_fans(self):
        user_fans = list(data_poster.get_user_fans(wrong_userId))
        my_fans = list(data_poster.get_user_fans(my_userId))
        assert user_fans == [] and my_fans != []

    def test_get_user_fans_withoffset(self):
        user_fans_page_1 = data_poster.get_user_fans_withoffset(
            wrong_userId, 1)
        my_fans_page_1 = data_poster.get_user_fans_withoffset(
            my_userId, 1)
        assert user_fans_page_1 == [] and my_fans_page_1 != []


if __name__ == '__main__':
    unittest.main()
