#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from lxml import etree
from urllib import request

from md_logging import *

setup_log()
write_log = logging.getLogger('Dimage')


class AutoImage(object):
    web_url = 'http://www.rentiyishu.in'
    theme_list = ['/zgrenti/', '/rbrenti/', '/omrenti/', '/ddrenti/', '/mnrenti/']
    local_path = 'img/'
    record_path = 'csv/'
    src_path = record_path + 'image_src.csv'

    def __init__(self):
        if not os.path.isdir(self.local_path):
            os.mkdir(self.local_path)
        if not os.path.isdir(self.record_path):
            os.mkdir(self.record_path)
        # 从网页获取所有主题的内容
        # all_index = []
        # for theme in self.theme_list:
        #     all_index += self.get_theme_index(theme, True)
        # 从文件获取所有主题的内容
        all_index = self.read_theme_index()
        print(all_index)
        # 从内容主页的列表获取图片链接
        for index in all_index:
            self.get_image_src(index, True)
        # 从文件读取图片链接并下载
        self.read_src_to_download()

    def get_theme_index(self, theme, save=False):
        cur_url = self.web_url + theme
        record_name = self.record_path + '{}.csv'.format(theme.replace('/', ''))
        index_list = []
        try:
            respond = request.urlopen(cur_url)
            page_source = respond.read().decode('utf-8')
            page_tree = etree.HTML(page_source)
            page_last_html = page_tree.xpath('//div[@class="page-show"]/ul/li/a[text()="末页"]/@href')[0]
            page_last = int(re.findall(r'\d+', page_last_html)[0])
            if save:
                with open(record_name, 'a+') as f:
                    f.write('{},{},{}\n'.format('地址', '数量', '名称'))
            for idx in range(1, page_last + 1):
                respond = request.urlopen(cur_url + '{}.html'.format(idx))
                page_source = respond.read().decode('utf-8')
                page_tree = etree.HTML(page_source)
                for li in page_tree.xpath('//ul[@class="detail-list"]/li'):
                    addr = li.xpath('a/@href')[0]
                    num = re.findall(r'\d+', li.xpath('div/span/text()')[0])[0]
                    name = li.xpath('a/@title')[0]
                    # print('地址：{} 数量：{} 名称：{}'.format(addr, num, name))
                    if save:
                        with open(record_name, 'a+') as f:
                            f.write('{},{},{}\n'.format(addr, num, name))
                    index_list.append(addr)
        except Exception as e:
            write_log.error('{}\n{}'.format(e, traceback.format_exc()))
        return index_list

    def read_theme_index(self):
        index_list = []
        try:
            for theme in self.theme_list:
                record_name = self.record_path + '{}.csv'.format(theme.replace('/', ''))
                if not os.path.isfile(record_name):
                    write_log.debug('read_theme_index {} not exist'.format(theme))
                    continue
                with open(record_name, 'r') as f:
                    while True:
                        line = f.readline().strip()
                        if not line:
                            break
                        if not re.match(r'.*\.html.*', line):
                            continue
                        index = line.split(',')[0]
                        index_list.append(index)
        except Exception as e:
            write_log.error('{}\n{}'.format(e, traceback.format_exc()))
        return index_list

    def get_image_src(self, image_url, save=False):
        src_list = []
        page_theme, page_suffix = os.path.split(image_url)
        page_theme += '/'
        if save:
            if not os.path.isfile(self.src_path):
                with open(self.src_path, 'w') as f:
                    f.write('IMAGE_SRC\n')
        while re.match(r'\d+.*\.html', page_suffix):
            page_url = self.web_url + page_theme + page_suffix
            try:
                respond = request.urlopen(page_url)
                page_source = respond.read().decode('utf-8')
                page_tree = etree.HTML(page_source)
                src = page_tree.xpath('//div[@id="bigpic"]/a/img/@src')[0]
                if save:
                    with open(self.src_path, 'a+') as f:
                        f.write('{}\n'.format(src))
                page_suffix = page_tree.xpath('//div[@class="page"]/ul/li/a[text()="下一页"]/@href')[0]
            except Exception as e:
                write_log.error('{}\n{}'.format(e, traceback.format_exc()))
        return src_list

    def download_image(self, dl_url, save_path):
        save_path = self.local_path + save_path
        try:
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
                self.download_image(download_url, os.path.basename(download_url))


if __name__ == '__main__':
    ai = AutoImage()
