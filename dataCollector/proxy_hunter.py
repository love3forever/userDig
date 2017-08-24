#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-08-24 09:01:27
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$

import requests
from bs4 import BeautifulSoup
from itertools import cycle
import time

proxy_source = 'http://www.kuaidaili.com/free/inha/{}/'

proxies = {
    "http": "",
    "https": "",
}


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
        if proxy_list:
            proxies = proxy_list[0].select('tr')
            for item in proxies[1:]:
                info = item.select('td')
                proxy_host = info[0].string
                proxy_port = info[1].string
                yield (proxy_host, proxy_port)


def gen_proxy():
    proxy_index = cycle(range(1, 20))
    for index in proxy_index:
        time.sleep(20)
        print('wating for new proxy')
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
        pass
    else:
        if test_response.status_code == 200:
            # print(test_response.content)
            test_soup = BeautifulSoup(test_response.content, 'lxml')
            ip_info = test_soup.select('.well')
            if ip_info:
                print(ip_info[0])


if __name__ == '__main__':
    proxy_pool = gen_proxy()
    times = 0
    for item in proxy_pool:
        test_proxy(item)
        times += 1
        if times > 100:
            break
