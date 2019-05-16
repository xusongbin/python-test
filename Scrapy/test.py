
import chardet
import urllib.request
from lxml import etree

url = 'http://2019.ip138.com/ic.asp'
req = urllib.request.Request(url)
resp = urllib.request.urlopen(req).read()
resp = resp.decode(chardet.detect(resp)['encoding'])
print(resp)
html = etree.HTML(resp)
# print(type(html))
html_data = html.xpath('//body/center[1]/text()')
print(html_data)

