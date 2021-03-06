# -*- coding: utf-8 -*-
# @Time    : 2019/3/30 9:42
# @Author  : 陈强
# @FileName: proxy_spiders.py
# @Software: PyCharm

"""
爬取代理ip网站，获取代理ip,并验证ip有效性
"""
import logging
import re

import threadpool

from ScrapyProxy.proxy_model import Proxy
from ScrapyProxy.config import available_proxy, VALIDATED_URL, headers
import requests
from lxml import etree


class ProxySpiders(object):
    def __init__(self):
        self.proxy_model_list = []
        # self.proxy_model = Proxy()

    def start(self):
        self.xici_spider()
        self.iphai_spider()
        self.data89ip_spider()
        self.kuaidaili_spider()
        self.filter_proxies()

    """
    function:使用线程池快速验证代理ip
    """
    def filter_proxies(self):
        # 默认10个线程
        pool = threadpool.ThreadPool(10)
        pool_requests = threadpool.makeRequests(self.filter_proxy, self.proxy_model_list)
        for req in pool_requests:
            pool.putRequest(req)
        pool.wait()
        print('---可用代理---%s' % len(available_proxy))

    """
    function：过滤无效代理
    """
    def filter_proxy(self, proxy_model):
        http_type = proxy_model.get_http_type()
        ip = proxy_model.get_ip()
        port = proxy_model.get_port()
        proxies = {
            http_type.lower(): http_type.lower() + "://" + ip + ":" + str(port)
        }
        try:
            response = requests.get(VALIDATED_URL, proxies=proxies, headers=headers, timeout=2)
            if response.status_code == 200:
                # 代理可用就将其加入到可用代理列表中
                available_proxy.append(proxy_model)
                return proxy_model
            else:
                return None
        except:
            return None
    """
    爬取西刺代理，如果爬虫失效，请修改相关xpath
    """
    def xici_spider(self):

        url = 'http://www.xicidaili.com/wt/1'  # 国内 HTTP 代理
        # url = 'http://www.xicidaili.com/wn/'   # 国内 HTTPS 代理

        agent = "xici"

        print('正在爬取西刺代理……')
        response = requests.get(url, headers=headers)
        selector = etree.HTML(response.text)
        infos = selector.xpath('//tr[@class="odd"]')

        for i, info in enumerate(infos):
            try:
                ip = info.xpath('./td[2]/text()')[0]  # ip
                port = info.xpath('./td[3]/text()')[0]  # 端口
                anonymity = info.xpath('./td[5]/text()')[0]  # 匿名度
                http_type = info.xpath('./td[6]/text()')[0]  # 类型
                area = info.xpath('./td[4]/a/text()')[0]  # 地区
                speed = info.xpath('./td[7]/div/@title')[0]  # 速度
                survival_time = info.xpath('./td[9]/text()')[0]  # 存活时间
                print(ip + " | " + port + " | " + anonymity + " | " + http_type + " | " + area + " | " + speed + " | " + survival_time)
                proxy = Proxy()
                proxy.set_ip(ip)
                proxy.set_port(port)
                proxy.set_http_type(http_type)
                proxy.set_anonymity(anonymity)
                # 处理空地区
                if area is None:
                    proxy.set_area('')
                else:
                    proxy.set_area(area)
                proxy.set_speed(speed)
                proxy.set_agent(agent)
                proxy.set_survival_time(survival_time)
                self.proxy_model_list.append(proxy)

            except Exception as e:
                logging.debug(e)

    def iphai_spider(self):
        url = 'http://www.iphai.com/free/ng'
        agent = "iphai"
        print('正在爬取IP海代理……')
        response = requests.get(url, headers=headers)
        response.encoding = response.apparent_encoding
        # print(response.text)
        selector = etree.HTML(response.text)
        for tr in selector.xpath('//div[@class="table-responsive module"]/table/tr'):
            try:
                ip = tr.xpath('td[1]/text()')[0].strip()
                port = tr.xpath('td[2]/text()')[0].strip()
                anonymity = tr.xpath('td[3]/text()')[0].strip()
                http_type = tr.xpath('td[4]/text()')[0].strip()
                area = tr.xpath('td[5]/text()')[0].strip()
                speed = tr.xpath('td[6]/text()')[0].strip()
                print(ip + " | " + port + " | " + anonymity + " | " + http_type + " | " + area + " | " + speed + " | ")
                proxy = Proxy()
                proxy.set_ip(ip)
                proxy.set_port(port)
                proxy.set_http_type(http_type)
                proxy.set_anonymity(anonymity)
                proxy.set_area(area)
                proxy.set_speed(speed)
                proxy.set_agent(agent)
                self.proxy_model_list.append(proxy)
            except Exception as e:
                logging.debug(e)

    def data89ip_spider(self):
        url = 'http://www.89ip.cn/'
        agent = "89ip"
        print('正在爬取89免费代理……')
        response = requests.get(url, headers=headers)
        selector = etree.HTML(response.text)
        for tr in selector.xpath('//table[@class="layui-table"]/tbody/tr'):
            try:
                ip = tr.xpath('td[1]/text()')[0].strip()
                port = tr.xpath('td[2]/text()')[0].strip()
                anonymity = '未知'
                http_type = 'HTTP'
                area = tr.xpath('td[3]/text()')[0].strip()
                speed = '未知'
                print(ip + " | " + port + " | " + anonymity + " | " + http_type + " | " + area + " | " + speed + " | ")
                proxy = Proxy()
                proxy.set_ip(ip)
                proxy.set_port(port)
                proxy.set_http_type(http_type)
                proxy.set_anonymity(anonymity)
                proxy.set_area(area)
                proxy.set_speed(speed)
                proxy.set_agent(agent)
                self.proxy_model_list.append(proxy)
            except Exception as e:
                logging.debug(e)

    def kuaidaili_spider(self):
        url = 'http://www.kuaidaili.com/free'
        agent = "快代理"
        print('正在爬取快代理……')
        response = requests.get(url, headers=headers)
        pattern = re.compile(
            '<tr>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>('
            '.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?</tr>',
            re.S)

        infos = re.findall(pattern, response.text)

        for item in infos:
            try:
                ip = item[0]  # ip
                port = item[1]  # 端口
                anonymity = item[2]  # 匿名度
                http_type = item[3]  # 类型
                area = item[4]  # 地区
                speed = item[5]  # 速度

                print(ip + " | " + port + " | " + anonymity + " | " + http_type + " | " + area + " | " + speed)

                if http_type == 'HTTP' or http_type == 'HTTPS':
                    # print(type.lower() + "://" + ip + ":" + port)
                    proxy = Proxy()
                    proxy.set_ip(ip)
                    proxy.set_port(port)
                    proxy.set_http_type(http_type.lower())
                    proxy.set_anonymity(anonymity)
                    proxy.set_area(area)
                    proxy.set_speed(speed)
                    proxy.set_agent(agent)
                    proxy.set_survival_time("")
                    self.proxy_model_list.append(proxy)
            except Exception as e:
                logging.debug(e)


if __name__ == '__main__':
    p = ProxySpiders()
    p.start()
    print('--------可用代理---------')
    print(available_proxy)
