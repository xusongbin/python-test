import scrapy
import json
from ScrapyHaoda.items import ScrapyhaodaItem

class GeturlSpider(scrapy.Spider):
    name = 'getUrl'
    allowed_domains = ['haoda2.net']
    # start_urls = [
    #     'http://haoda2.net/xvcg/page',
    #     # 'http://haoda2.net/casd/page',
    #     # 'http://haoda2.net/htgf/page',
    #     # 'http://haoda2.net/asda/page',
    #     # 'http://haoda2.net/dfsa/page'
    # ]
    start_urls = ['https://haoda2.net']

    def parse(self, response):
        assert isinstance(response, scrapy.http.Response)
        print(response.url)
        # 1.判断是否为首页，获取更多page详情
        if response.url == self.start_urls[0]:
            for each in response.xpath("//div[@class='col-md-12']/div"):
                _page = each.xpath("p/a/@href").extract_first()
                yield scrapy.Request(response.urljoin(_page), callback=self.parse)
        # 2.page详情页，获取每个视频的网页链接
        if response.xpath("//div[@class='movie']"):
            for row in response.xpath("//div[@class='movie']/div"):    # row
                for col in row.xpath("div"):    # col
                    _href = col.xpath("div/a/@href").extract_first()
                    yield scrapy.Request(response.urljoin(_href), callback=self.parse)
        # 3.获取url
        _page = response.url[len(self.start_urls[0])+1:].split('/')[0]
        if response.url.split('/')[-1] == 'play':
            item = ScrapyhaodaItem()
            _text = response.text
            _text = _text[_text.find('video: {'):]
            _video = _text[_text.find('url')+6:]
            _video = _video[:_video.find('\'')]
            _pic = _text[_text.find('pic')+6:]
            _pic = _pic[:_pic.find('\'')]
            _name = response.xpath("//h3[@class='media-heading MovieName']/text()").extract_first().strip()
            item['type'] = 'url'
            item['page'] = _page
            item['video'] = _video
            item['name'] = _name
            item['pic'] = _pic
            print('{} {} {} {}'.format(_page, _video, _name, _pic))
            yield item
        # 4.获取下一页
        _text = response.text
        if '下一页' in _text and '尾页' in _text:
            try:
                next_page = _text[:_text.rfind('">下一页</a')]
                next_page = next_page[next_page.rfind("'page':")+9:]
                next_page = next_page[:next_page.find("'")]
                end_page = _text[:_text.rfind('">尾页</a')]
                end_page = end_page[end_page.rfind("'page':")+9:]
                end_page = end_page[:end_page.find("'")]
                if next_page != end_page:
                    next_url = response.urljoin('./page?page={}'.format(next_page))
                    # print(next_url)
                    yield scrapy.Request(next_url, callback=self.parse)
            except Exception as e:
                _ = e



