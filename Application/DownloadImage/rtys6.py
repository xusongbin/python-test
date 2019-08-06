#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from time import sleep
from lxml import etree
from urllib import request
from urllib import parse

from md_logging import *

setup_log()
write_log = logging.getLogger('Dimage')


class AutoImage(object):
    web_url = 'http://rtys6.com'
    theme_list = ['/ArtZG/', '/ArtOM/', '/ArtRB/', '/ArtDD/', '/ArtZXY/', '/ArtMET/']
    img_base_path = 'img/'
    csv_base_path = 'csv/'
    record_path = csv_base_path + 'rtys6_record.csv'
    src_path = csv_base_path + 'rtys6_src.csv'
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

    def __init__(self):
        if not os.path.isdir(self.img_base_path):
            os.mkdir(self.img_base_path)
        if not os.path.isdir(self.csv_base_path):
            os.mkdir(self.csv_base_path)
        # 使用代理
        # proxy_support = request.ProxyHandler({'http': '112.95.207.53:8888'})
        # opener = request.build_opener(proxy_support)
        # request.install_opener(opener)
        # 从网页获取所有主题的内容
        # for theme in self.theme_list:
        #     self.get_theme_index(theme, True)
        # 从文件获取所有主题的内容
        # data_list = self.read_theme_index()
        # 从内容主页的列表获取图片链接
        # test_url = self.web_url + data_list[0][0]
        # print('打开连接：{}'.format(test_url))
        # print(self.get_source_by_url(test_url))
        # for index, name in data_list:
        #     self.get_image_src(index, name, True)
        # 从文件读取图片链接并下载
        # self.read_src_to_download()
        # self.download_image('https://p.666ho.com/pic/2018/0601/678-lp.jpg', '1.jpg')

    def get_source_by_url(self, surl, retry=4, method='GET'):
        while retry > 0:
            retry -= 1
            try:
                if method == 'GET':
                    req = request.Request(surl, headers=self.headers)
                    respond = request.urlopen(req, timeout=3)
                    page_source = respond.read().decode('utf-8')
                    return page_source
                else:
                    data = {'method': 0, 'host': surl, 'hideRAW': ''}
                    data = parse.urlencode(data).encode('utf-8')
                    req = request.Request('http://tool.chinaz.com/Tools/httptest.aspx', data=data, headers=self.headers)
                    respond = request.urlopen(req, timeout=3)
                    page_source = respond.read().decode('utf-8')
                    page_tree = etree.HTML(page_source)
                    page_context = page_tree.xpath('//div[@class="RtitCeCode"]/pre/text()')[0]
                    return page_context
            except Exception as e:
                pass
            if method == 'GET':
                method = 'POST'
            else:
                method = 'GET'
        return None

    def get_theme_index(self, theme, save=False):
        root_url = self.web_url + theme
        write_log.debug('获取主题：{} 的所有专辑'.format(theme))
        index_list = []
        if save:
            if not os.path.isfile(self.record_path):
                with open(self.record_path, 'w') as f:
                    f.write('{},{},{}\n'.format('地址', '数量', '名称'))
        cur_url = root_url
        while cur_url:
            try:
                page_source = self.get_source_by_url(cur_url)
                # print(page_source)
                if not page_source:
                    write_log.error('get_theme_index: get source failure')
                    return index_list
                page_tree = etree.HTML(page_source)
                page_next_html = page_tree.xpath('//div[@class="pagelist"]/a[text()="下一页"]/@href')[0]
                # print('下一页：{}'.format(page_next_html))
                cur_url = root_url + page_next_html
            except:
                break
            try:
                for li in page_tree.xpath('//div[@class="fzltp"]/ul/li'):
                    addr = li.xpath('a/@href')[0]
                    name = li.xpath('a/img/@alt')[0]
                    write_log.debug('地址：{} 名称：{}'.format(addr, name))
                    if save:
                        with open(self.record_path, 'a+') as f:
                            f.write('{},{}\n'.format(addr, name))
                    index_list.append(addr)
            except Exception as e:
                print('{}\n{}'.format(e, traceback.format_exc()))
                cur_url = None
        return index_list

    def read_theme_index(self):
        data_list = []
        try:
            with open(self.record_path, 'r') as f:
                while True:
                    line = f.readline().strip()
                    if not line:
                        break
                    if not re.match(r'/.*/\d+/', line):
                        continue
                    line_list = line.split(',')
                    data_list.append((line_list[0], line_list[1]))
                    print('read_theme_index: {} {}'.format(line_list[0], line_list[1]))
        except Exception as e:
            write_log.error('{}\n{}'.format(e, traceback.format_exc()))
        return data_list

    def get_image_src(self, image_url, name, save=False):
        src_list = []
        page_theme, page_suffix = os.path.split(image_url)
        page_theme += '/'
        if save:
            if not os.path.isfile(self.src_path):
                with open(self.src_path, 'w') as f:
                    f.write('IMAGE_SRC\n')
        write_log.debug('get_image_src:{} {}'.format(image_url, name))
        while re.match(r'\d+.*\.html', page_suffix):
            page_url = self.web_url + page_theme + page_suffix
            page_source = ''
            try:
                page_source = self.get_source_by_url(page_url)
                if not page_source:
                    write_log.error('get_image_src: get source failure')
                    return src_list
                if 'bigpic' not in page_source:
                    return src_list
                page_tree = etree.HTML(page_source)
                src = page_tree.xpath('//div[@id="bigpic"]/a/img/@src')[0]
                write_log.debug('get_image_src:{} {}'.format(page_url, src))
                if save:
                    with open(self.src_path, 'a+') as f:
                        f.write('{}\n'.format(src))
                page_suffix = page_tree.xpath('//div[@class="page"]/ul/li/a[text()="下一页"]/@href')[0]
            except Exception as e:
                if page_source:
                    write_log.debug(page_source)
                write_log.error('{}\n{}'.format(e, traceback.format_exc()))
                write_log.debug('get_image_src:{} {}'.format(page_url, 'ERROR'))
                return src_list
        return src_list

    def download_image(self, dl_url, save_path, retry=5):
        save_path = self.img_base_path + save_path
        try:
            while retry > 0:
                retry -= 1
                request.urlretrieve(dl_url, save_path)
                return True
        except Exception as e:
            write_log.error('{}\n{}'.format(e, traceback.format_exc()))
        return False

    def read_src_to_download(self):
        if not os.path.isfile(self.src_path):
            write_log.error('图片链接文件不存在！')
            return False
        with open(self.src_path, 'r') as f:
            while True:
                line = f.readline().strip()
                if not line:
                    break
                if not re.match(r'/uploads/allimg/\d+/.*\..*', line):
                    continue
                download_url = self.web_url + line
                download_name = os.path.basename(download_url)
                sta = self.download_image(download_url, download_name)
                result = '成功' if sta else '失败'
                write_log.debug('download_name: {} {}'.format(download_name, result))


if __name__ == '__main__':
    ai = AutoImage()
    sleep(5)
