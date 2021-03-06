#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import gzip
import socket
from time import sleep
from lxml import etree
from urllib import request
from urllib import parse
import gevent
from gevent import monkey
monkey.patch_socket()
socket.setdefaulttimeout(20)

from md_logging import *

setup_log()
write_log = logging.getLogger('IMAGE')


class AutoImage(object):
    info_rtys6 = {
        'src_file': 'src_rtys6.csv',
        'index_file': 'index_rtys6.csv',
        'url_head': 'http://rtys6.com',
        'url': [
            'http://rtys6.com/ArtZG/',
            'http://rtys6.com/ArtOM/',
            'http://rtys6.com/ArtRB/',
            'http://rtys6.com/ArtDD/',
            'http://rtys6.com/ArtZXY/',
            'http://rtys6.com/ArtMET/'
        ]
    }
    info_rentiyishu = {
        'src_file': 'src_rentiyishu.csv',
        'index_file': 'index_rentiyishu.csv',
        'url_head': 'http://www.rentiyishu.in',
        'url': [
            'http://www.rentiyishu.in/zgrenti/',
            'http://www.rentiyishu.in/rbrenti/',
            'http://www.rentiyishu.in/omrenti/',
            'http://www.rentiyishu.in/ddrenti/',
            'http://www.rentiyishu.in/mnrenti/',
        ]
    }
    info_mm131 = {
        'src_file': 'src_mm131.csv',
        'index_file': 'index_mm131.csv',
        'url_head': 'https://mm131.one',
        'url': [
        ]
    }
    headers = {
        'User-Agent': (
                'Mozilla/5.0 '
                '(Windows NT 6.1; WOW64) '
                'AppleWebKit/537.36 '
                '(KHTML, like Gecko) '
                'Chrome/70.0.3538.25 '
                'Safari/537.36 Core/1.70.3722.400 '
                'QQBrowser/10.5.3738.400'
            )
    }
    # 使用代理
    # proxy_support = request.ProxyHandler({'http': '112.95.207.53:8888'})
    # opener = request.build_opener(proxy_support)
    # request.install_opener(opener)

    def __init__(self):
        self.download_skip = 0
        self.download_pass = 0
        self.download_fail = 0
        # self.test_request()
        # 获取地址信息
        self.do_rtys6_save_src(True, True)
        self.do_rentiyishu_save_src(False, True)
        self.do_mm131_save_src(True, True)
        # 从文件读取图片链接并下载
        src_file = self.info_rtys6['src_file']
        self.do_readlink_to_download(src_file, False)

    def test_request(self):
        url = 'https://mm131.one/listpage/3.html'
        req = request.Request(url, headers=self.headers)
        respond = request.urlopen(req, timeout=5)
        # <meta charset="UTF-8">
        code = 'UTF-8'
        if 'charset=' in respond.info().get('Content-Type'):
            code = respond.info().get('Content-Type')
            code = code[code.find('charset=')+8:]
        if respond.info().get('Content-Encoding') == 'gzip':
            page_source = gzip.decompress(respond.read()).decode(code, 'ignore')
        else:
            page_source = respond.read().decode(code, 'ignore')
        print(page_source)
        return page_source
    
    def do_rtys6_save_src_gevent(self, this_url, this_name):
        src_file = self.info_rtys6['src_file']
        # 获取专辑源码
        try:
            page_source = self.do_request_page(this_url)
            if not page_source:
                write_log.debug('获取专辑：{} 源码异常'.format(this_url))
                return
            page_tree = etree.HTML(page_source)
            num = page_tree.xpath('//div[@class="tpm01"]/p/font[@color="blue"]/text()')[2]
            num = int(re.findall(r'\d+', num)[0])
            if num < 1:
                write_log.debug('获取专辑：{} 页码异常'.format(this_url))
                return
        except Exception as e:
            write_log.debug('获取专辑：{} 处理异常'.format(this_url))
            write_log.error('{}\n{}'.format(e, traceback.format_exc()))
            return
        write_log.debug('获取专辑：{} {} {}'.format(this_url, num, this_name))
        idx = 1
        while idx < num:
            page_url = this_url + '{}.html'.format(idx)
            page_source = self.do_request_page(page_url)
            if not page_source:
                write_log.debug('获取链接：{} 源码异常'.format(page_url))
                continue
            page_tree = etree.HTML(page_source)
            for li in page_tree.xpath('//div[@class="www"]/li'):
                src = li.xpath('a/img/@src|span/img/@src')[0]
                src = src.replace('-lp', '').replace('-LP', '')
                write_log.debug('获取链接：{}'.format(src))
                with open(src_file, 'a+') as f:
                    f.write('{}\n'.format(src))
                try:
                    page_name = li.xpath('a/@href')[0]
                    idx = int(re.findall(r'\d+', page_name)[0]) + 1
                except Exception as e:
                    pass

    def do_rtys6_save_src_by_index(self):
        index_file = self.info_rtys6['index_file']
        if not os.path.isfile(index_file):
            write_log.error('主页链接文件不存在！')
            return False
        t = []
        with open(index_file, 'r') as index_fd:
            while True:
                line = index_fd.readline()
                if not line:
                    if len(t) > 0:
                        gevent.joinall(t)
                        request.urlcleanup()
                    break
                line = line.strip()
                if not line or not re.match(r'https?://rtys6\.com/.*,.*', line):
                    continue
                this_url = line.split(',')[0]
                this_name = line.split(',')[1]
                t.append(gevent.spawn(self.do_rtys6_save_src_gevent, this_url, this_name))
                if len(t) >= 10:
                    gevent.joinall(t)
                    request.urlcleanup()
                    t = []
        return

    def do_rtys6_save_index(self):
        url_list = self.info_rtys6['url']
        url_head = self.info_rtys6['url_head']
        index_file = self.info_rtys6['index_file']
        if os.path.isfile(index_file):
            os.remove(index_file)
        for root_url in url_list:
            cur_url = root_url
            while cur_url:
                try:
                    page_source = self.do_request_page(cur_url)
                    if not page_source:
                        write_log.debug('爬取url：{} 获取源码失败'.format(cur_url))
                        break
                    page_tree = etree.HTML(page_source)
                    page_next_html = page_tree.xpath('//div[@class="pagelist"]/a[text()="下一页"]/@href')[0]
                    next_url = root_url + page_next_html
                    write_log.debug('爬取url：{} 成功'.format(cur_url))
                except Exception as e:
                    write_log.debug('爬取url：{} 异常'.format(cur_url))
                    print('{}\n{}'.format(e, traceback.format_exc()))
                    break
                try:
                    for li in page_tree.xpath('//div[@class="fzltp"]/ul/li'):
                        addr = li.xpath('a/@href')[0]
                        addr = url_head + addr
                        name = li.xpath('a/img/@alt')[0]
                        write_log.debug('爬取内容： {} {}'.format(addr, name))
                        with open(index_file, 'a+') as f:
                            f.write('{},{}\n'.format(addr, name))
                except Exception as e:
                    print('{}\n{}'.format(e, traceback.format_exc()))
                cur_url = next_url

    def do_rtys6_save_src(self, index=True, src=True):
        # 从网页获取所有主题的内容
        if index:
            self.do_rtys6_save_index()
        # 从内容主页的列表获取图片链接
        if src:
            self.do_rtys6_save_src_by_index()

    def do_rentiyishu_save_src_by_index(self):
        url_head = self.info_rentiyishu['url_head']
        src_file = self.info_rentiyishu['src_file']
        index_file = self.info_rentiyishu['index_file']
        if not os.path.isfile(index_file):
            write_log.error('主页链接文件不存在！')
            return False
        with open(index_file, 'r') as index_fd:
            while True:
                line = index_fd.readline()
                if not line:
                    break
                line = line.strip()
                if not line or not re.match(r'https?://www\.rentiyishu\.in/.*,.*,.*', line):
                    continue
                this_url = line.split(',')[0]
                this_num = line.split(',')[1]
                this_name = line.split(',')[2]
                url_base = this_url[:this_url.rfind('/')] + '/'
                url_name = this_url[this_url.rfind('/'):]
                write_log.debug('当前地址：{} {} {}'.format(this_url, this_num, this_name))
                while True:
                    cur_url = url_base + url_name
                    try:
                        page_source = self.do_request_page(cur_url)
                        if not page_source:
                            break
                        if 'bigpic' not in page_source:
                            break
                        page_tree = etree.HTML(page_source)
                        src = page_tree.xpath('//div[@id="bigpic"]/a/img/@src')[0]
                        src = url_head + src
                        write_log.debug('获取链接：{}'.format(src))
                        with open(src_file, 'a+') as f:
                            f.write('{}\n'.format(src))
                        url_name = page_tree.xpath('//div[@class="page"]/ul/li/a[text()="下一页"]/@href')[0]
                    except Exception as e:
                        write_log.debug('获取链接：{} 处理异常'.format(src))
                        write_log.error('{}\n{}'.format(e, traceback.format_exc()))
                        break

    def do_rentiyishu_save_index(self):
        url_list = self.info_rentiyishu['url']
        url_head = self.info_rentiyishu['url_head']
        index_file = self.info_rentiyishu['index_file']
        if os.path.isfile(index_file):
            os.remove(index_file)
        for root_url in url_list:
            try:
                page_source = self.do_request_page(root_url)
                if not page_source:
                    write_log.debug('爬取url：{} 获取源码失败'.format(root_url))
                    continue
                page_tree = etree.HTML(page_source)
                page_last_html = page_tree.xpath('//div[@class="page-show"]/ul/li/a[text()="末页"]/@href')[0]
                page_last = int(re.findall(r'\d+', page_last_html)[0])
            except Exception as e:
                write_log.debug('爬取url：{} 处理异常'.format(root_url))
                write_log.error('{}\n{}'.format(e, traceback.format_exc()))
                continue
            for idx in range(1, page_last + 1):
                cur_url = root_url + '{}.html'.format(idx)
                try:
                    page_source = self.do_request_page(cur_url)
                    if not page_source:
                        write_log.debug('爬取url：{} 获取源码失败'.format(root_url))
                        continue
                    page_tree = etree.HTML(page_source)
                    for li in page_tree.xpath('//ul[@class="detail-list"]/li'):
                        addr = li.xpath('a/@href')[0]
                        addr = url_head + addr
                        num = re.findall(r'\d+', li.xpath('div/span/text()')[0])[0]
                        name = li.xpath('a/@title')[0]
                        write_log.debug('爬取内容： {} {} {}'.format(addr, num, name))
                        with open(index_file, 'a+') as f:
                            f.write('{},{},{}\n'.format(addr, num, name))
                except Exception as e:
                    write_log.error('{}\n{}'.format(e, traceback.format_exc()))

    def do_rentiyishu_save_src(self, index=True, src=True):
        # 从网页获取所有主题的内容
        if index:
            self.do_rentiyishu_save_index()
        # 从内容主页的列表获取图片链接
        if src:
            self.do_rentiyishu_save_src_by_index()

    def do_mm131_save_src_gevent(self, this_url, this_name):
        url_head = self.info_mm131['url_head']
        src_file = self.info_mm131['src_file']
        try:
            page_source = self.do_request_page(this_url)
            if not page_source:
                return
            page_tree = etree.HTML(page_source)
            for a in page_tree.xpath('//div[@class="img gets"]/center/a'):
                for src in a.xpath('img/@src'):
                    src = src.strip()
                    if not src:
                        continue
                    image_src = url_head + src
                    write_log.debug('获取链接：{}'.format(image_src))
                    with open(src_file, 'a+') as f:
                        f.write('{}\n'.format(image_src))
        except Exception as e:
            write_log.debug('获取链接：{} 处理异常'.format(this_url))
            write_log.error('{}\n{}'.format(e, traceback.format_exc()))
            return

    def do_mm131_save_src_by_index(self):
        index_file = self.info_mm131['index_file']
        if not os.path.isfile(index_file):
            write_log.error('主页链接文件不存在！')
            return False
        t = []
        with open(index_file, 'r') as index_fd:
            while True:
                line = index_fd.readline()
                if not line:
                    if len(t) > 0:
                        gevent.joinall(t)
                        request.urlcleanup()
                    break
                line = line.strip()
                if not line or not re.match(r'https?://mm131.one/mm/.*\.html,.*', line):
                    continue
                this_url = line.split(',')[0]
                this_name = line.split(',')[1]
                write_log.debug('当前地址：{} {}'.format(this_url, this_name))
                t.append(gevent.spawn(self.do_mm131_save_src_gevent, this_url, this_name))
                if len(t) >= 10:
                    gevent.joinall(t)
                    request.urlcleanup()
                    t = []

    def do_mm131_save_index(self):
        url_head = self.info_mm131['url_head']
        index_file = self.info_mm131['index_file']
        if os.path.isfile(index_file):
            os.remove(index_file)
        for theme_idx in range(1, 2820):
            album_url = url_head + '/mm/{}.html'.format(theme_idx)
            page_source = self.do_request_page(album_url)
            if not page_source:
                write_log.debug('爬取url：{} 获取源码失败'.format(album_url))
                continue
            try:
                page_tree = etree.HTML(page_source)
                album_name = page_tree.xpath('//h1/text()')[0]
                with open(index_file, 'a+') as f:
                    f.write('{},{}\n'.format(album_url, album_name))
                # write_log.debug('爬取内容： {} {}'.format(album_url, album_name))
                idx_str = page_tree.xpath('//div[@class="pagebread"]/li[1]/a/text()')[0]
                last_idx = int(re.findall(r'\d+', idx_str)[0])
            except:
                continue
            for next_dix in range(2, last_idx):
                album_url = url_head + '/mm/{}_{}.html'.format(theme_idx, next_dix)
                with open(index_file, 'a+') as f:
                    f.write('{},{}\n'.format(album_url, album_name))
                # write_log.debug('爬取内容： {} {}'.format(album_url, album_name))

    def do_mm131_save_src(self, index=True, src=True):
        # 从网页获取所有主题的内容
        if index:
            self.do_mm131_save_index()
        # 从内容主页的列表获取图片链接
        if src:
            self.do_mm131_save_src_by_index()

    def do_request_page(self, surl):
        try:
            req = request.Request(surl, headers=self.headers)
            respond = request.urlopen(req, timeout=5)
            code = 'UTF-8'
            if 'charset=' in respond.info().get('Content-Type'):
                code = respond.info().get('Content-Type')
                code = code[code.find('charset=') + 8:]
            if respond.info().get('Content-Encoding') == 'gzip':
                page_source = gzip.decompress(respond.read()).decode(code, 'ignore')
            else:
                page_source = respond.read().decode(code, 'ignore')
            return page_source
        except:
            pass
        try:
            headers = self.headers
            headers['Host'] = 'tool.chinaz.com'
            headers['Origin'] = 'http://tool.chinaz.com'
            headers['Referer'] = 'http://tool.chinaz.com/Tools/httptest.aspx'
            data = {'method': 0, 'host': surl.split(':')[1][2:], 'hideRAW': ''}
            data = parse.urlencode(data).encode('utf-8')
            req = request.Request('http://tool.chinaz.com/Tools/httptest.aspx', data=data, headers=headers)
            respond = request.urlopen(req, timeout=5)
            page_source = respond.read().decode('utf-8', 'ignore')
            page_tree = etree.HTML(page_source)
            page_context = page_tree.xpath('//div[@class="RtitCeCode"]/pre/text()')[0]
            return page_context
        except:
            pass
        return None

    def do_download_gevent(self, dl_url, save_path, save_name, instead=False):
        # 创建文件路径
        cur_path = ''
        for name in save_path.split('/'):
            cur_path += name + '/'
            if not os.path.isdir(cur_path):
                os.mkdir(cur_path)
        save_url = '{}/{}'.format(save_path, save_name)
        # 未强制替换文件则判断文件是否存在
        if not instead and os.path.isfile(save_url):
            write_log.debug('do_download_gevent: {} 已存在'.format(save_url))
            self.download_skip += 1
            return
        try:
            dl_url = dl_url.replace(' ', '%20')
            request.urlretrieve(dl_url, save_url)
            request.urlcleanup()
            write_log.debug('do_download_gevent: {} 成功'.format(dl_url))
            self.download_pass += 1
            return
        except Exception as e:
            pass
        self.download_fail += 1
        write_log.debug('do_download_gevent: {} 失败'.format(dl_url))

    def do_readlink_to_download(self, link_path, instead=False):
        if not os.path.isfile(link_path):
            write_log.error('图片链接文件不存在！')
            return False
        t = []
        self.download_skip = 0
        self.download_pass = 0
        self.download_fail = 0
        with open(link_path, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    if len(t) > 0:
                        gevent.joinall(t)
                    break
                line = line.strip()
                if not re.match(r'.*\.jpg', line):
                    continue
                remote_url = line
                download_path, download_name = os.path.split(line)
                download_path = download_path.replace('http://', '')
                download_path = download_path.replace('https://', '')
                t.append(gevent.spawn(self.do_download_gevent, remote_url, download_path, download_name, instead))
                if len(t) >= 120:
                    gevent.joinall(t, timeout=60)
                    t = []
        write_log.info('下载结束： PASS={} FAIL={} SKIP={}'.format(
            self.download_pass, self.download_fail, self.download_skip
        ))


if __name__ == '__main__':
    ai = AutoImage()
    # sleep(5)
