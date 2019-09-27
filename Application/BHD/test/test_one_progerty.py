
import gzip
from urllib import request
from lxml import etree

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': (
        'language=zh-CN; '
        'sd7038915=q9mjqnc651daad8i6gpum1uqf7; '
        'loginName=mark3333520%40163.com; '
        'loginPwd=f3in2oWmp61%2F'
        'dHqnfanUzo6oqWKMjKnOl4h%2B'
        'mK7LlNyMi6zNhsy3rX9igmOKqLbcg6W4qoCvg8qAZ3%2F'
        'Pv7WVzYyhq9qGtrtoiqqSp324q86BqLmega97zoBne8u%2F'
        'pZySgXu3mJHPrKN%2FqoJkic6rz47LvZ98o2Wf;'
    ),
    'Host': 'www.onepool.co',
    'Referer': 'http://www.onepool.co/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 6.1; WOW64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3676.400 QQBrowser/10.4.3469.400'
    )
}

url = 'http://www.onepool.co/home/user/asset.html'

req = request.Request(url, headers=headers)
resp = request.urlopen(req, timeout=3)
context = resp.read()
if resp.info().get('Content-Encoding') == 'gzip':
    context = gzip.decompress(context).decode('utf-8')
else:
    context = context.decode('utf-8')
html = etree.HTML(context)
data_progerty = html.xpath('//div[@class="layui-tab-content"]/div[1]/div/table/tbody/tr')
data_matters = html.xpath('//div[@class="layui-tab-content"]/div[2]/div/table/tbody/tr')

for tr in data_progerty:
    print(tr.xpath('td[1]/lan/@t'))
    print('{}:{}'.format(tr.xpath('td[1]/text()')[1].strip().split(' ')[0],
                         tr.xpath('td[4]/text()')[0]))

for tr in data_matters:
    print('{}:{}'.format(tr.xpath('td[1]/text()')[1].strip().split(' ')[0],
                         tr.xpath('td[4]/text()')[0]))
