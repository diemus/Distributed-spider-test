from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from scrapy_redis.spiders import RedisCrawlSpider
from items import MyItem
from scrapy.spiders import CrawlSpider


class MyCrawler(RedisCrawlSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'jsl'
    redis_key = 'jsl:start_urls'

    page_links=LinkExtractor(allow=(r'www.jisilu.cn/people/list/sort_key-__page-\d+'))

    rules = (
        # 获取所有页面链接
        Rule(page_links,callback='parse_page', follow=True),
    )

    #def __init__(self, *args, **kwargs):
    #     动态定义 allowed domains.
    #    domain = kwargs.pop('domain', '')
    #    self.allowed_domains = filter(None, domain.split(','))
    #    super(MyCrawler, self).__init__(*args, **kwargs)

    def parse_page(self, response):

        ret = response.xpath(r'//div[@class="aw-item"]')
        for i in ret:
            item = MyItem()
            # 图片链接，对相对链接做修改
            image_urls = i.xpath('./a[contains(@class,"aw-user-img")]//img/@src').extract_first()

            item['image_urls'] = image_urls
            item['name'] = i.xpath('.//a[@class="aw-user-name"]/text()').extract_first()
            print(item)
            yield item



