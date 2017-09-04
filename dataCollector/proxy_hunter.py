#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-08-24 09:01:27
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$

import requests
from bs4 import BeautifulSoup
from itertools import cycle, count
import time
from datetime import datetime, timedelta
from threading import Thread

proxy_source = 'http://www.kuaidaili.com/ops/proxylist/{}/'
kuaidaili = ''

proxies = {
    "http": "",
    "https": "",
}

#  普通代理


def get_proxy_address(index):
    proxy_url = proxy_source.format(index)
    try:
        proxy_page = requests.get(proxy_url, timeout=5)
    except Exception as e:
        print(str(e))
    else:
        print(proxy_url)
        print(proxy_page.status_code)
        proxy_soup = BeautifulSoup(proxy_page.content, 'lxml')
        proxy_list = proxy_soup.select('.con-body')
        for item in proxy_list:
            h2 = item.select('h2')
            if h2 and u'免费高速HTTP代理IP列表' in h2[0].string:
                proxies = item.select('tr')
                for item in proxies[1:]:
                    info = item.select('td')
                    proxy_host = info[0].string
                    proxy_port = info[1].string
                    yield (proxy_host, proxy_port)


def gen_proxy():
    proxy_index = cycle(range(1, 11))
    for index in proxy_index:
        print('wating for new proxy')
        time.sleep(20)
        proxy_production = get_proxy_address(index)
        for proxy_pair in proxy_production:
            yield proxy_pair


def test_proxy(proxy_pair):
    proxies['http'] = "http://{}:{}".format(*proxy_pair)
    proxies['https'] = "http://{}:{}".format(*proxy_pair)
    print('testing proxy:{}:{}'.format(*proxy_pair))
    try:
        test_response = requests.get(
            'http://ip.cn/', timeout=5, proxies=proxies)
    except Exception as e:
        print(str(e))
        return False
    else:
        if test_response.status_code == 200:
            # print(test_response.content)
            test_soup = BeautifulSoup(test_response.content, 'lxml')
            ip_info = test_soup.select('.well')
            if ip_info:
                print(ip_info[0])
                return True
        else:
            print(test_response.status_code)
            return False


# 快代理
def gen_kuaidaili():
    counter = count()
    for index in counter:
        time.sleep(5)
        proxy_data = requests.get(kuaidaili)
        proxy_text = proxy_data.text
        proxy_pool = proxy_text.split('\r\n')
        for proxy in proxy_pool:
            yield tuple(proxy.split(':'))


def gen_myproxy():
    my_host = cycle(['eclipsesv.com', 'git.eclipsesv.com',
                     'service.eclipsesv.com', ''])
    cold_down = {}
    cold_time = timedelta(minutes=15)
    default_cold = timedelta(minutes=14)
    for host in my_host:
        last_use_time = cold_down.setdefault(
            host, datetime.now() - default_cold)
        if datetime.now() - last_use_time >= cold_time:
            yield (host, 8899)
            cold_down[host, datetime.now()]
        else:
            time_remaining = (cold_time - (datetime.now() -
                                           last_use_time)).total_seconds()
            waiting_cold_down = Thread(
                target=counting_down, args=(time_remaining,))
            waiting_cold_down.start()
            time.sleep(time_remaining)
            if host:
                yield (host, 8899)
            else:
                yield ('', '')
            cold_down[host] = datetime.now()


def counting_down(seconds=0):
    seconds = int(seconds)
    while True:
        if seconds > 0:
            print('cold down in {} seconds'.format(seconds))
            time.sleep(5)
            seconds -= 5
        else:
            break


if __name__ == '__main__':
    # 普通代理测试
    # proxy_pool = gen_kuaidaili()
    # times = 0
    # for item in proxy_pool:
    #     test_proxy(item)
    #     times += 1
    #     if times > 100:
    #         break

    # 快代理测试
    # kdy = gen_kuaidaili()
    # for i in range(201):
    #     print next(kdy)

    # 自建代理
    my_proxy = gen_myproxy()
    for proxy in my_proxy:
        print(proxy)
