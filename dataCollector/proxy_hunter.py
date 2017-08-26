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

proxy_source = 'http://www.kuaidaili.com/ops/proxylist/{}/'
kuaidaili = 'http://dev.kuaidaili.com/api/getproxy/?orderid=940357427810641&num=300&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=2&method=2&an_ha=1&sep=1'

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


if __name__ == '__main__':
    # 普通代理测试
    proxy_pool = gen_kuaidaili()
    times = 0
    for item in proxy_pool:
        test_proxy(item)
        times += 1
        if times > 100:
            break

    # 快代理测试
    # kdy = gen_kuaidaili()
    # for i in range(201):
    #     print next(kdy)
