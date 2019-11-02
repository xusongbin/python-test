
import sys
from lxml import etree
from urllib import request
from time import time

from show_tips import show_tooltip


class App(object):
    code = 'JDVA00834400907'
    url = 'http://www.jdwl.com/order/search?waybillCodes={}'.format(code)
    show = ''
    tout = 0

    def __init__(self):
        self.run()

    def run(self):
        while True:
            text = self.get_content()
            if not text:
                continue
            if self.show != text:
                self.show = text
                print(self.show)
                show_tooltip("物流更新", self.show)

    def get_content(self):
        if time() - self.tout < 10:
            return None
        self.tout = time()

        text = ''
        try:
            resp = request.urlopen(self.url, timeout=3)
            context = resp.read().decode('utf-8')
            html = etree.HTML(context)
            for li in html.xpath('//div[@class="r-body"]/ul/li'):
                for div in li.xpath('div/div'):
                    text += '{} {} {}\r\n'.format(li.xpath('span/text()')[0],
                                                  div.xpath('span/text()')[0],
                                                  div.xpath('p/text()')[0].strip())
            return text.strip()
        except:
            return None


if __name__ == '__main__':
    app = App()
