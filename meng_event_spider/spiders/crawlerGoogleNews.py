import scrapy
from scrapy.linkextractor import LinkExtractor
from scrapy.spiders.crawl import CrawlSpider, Rule
from twisted.internet import reactor
# from scrapy_splash import SplashRequest
from collections import OrderedDict
import re
from mengEventProject.items import MengEventItem

class googleNewsSpider(CrawlSpider):

    name = "googleNewsSpider"
    allowed_domain = ["news.google.com"]

    def start_requests(self):

        start_urls = ["https://news.google.com/search?q=meng+wanzhou+site:www3.nhk.or.jp/nhkworld/",
                      "https://news.google.com/search?q=meng+wanzhou+site:www.aljazeera.com/",
                      "https://news.google.com/search?q=meng+wanzhou+site:www.bbc.co.uk",
                      "https://news.google.com/search?q=meng+wanzhou+site:uk.reuters.com/",
                      "https://news.google.com/search?q=meng+wanzhou+site:tass.ru/en",
                      "https://news.google.com/search?q=meng+wanzhou+site:abcnews.go.com/",
                      "https://news.google.com/search?q=meng+wanzhou+site:www.cbsnews.com/",
                      "https://news.google.com/search?q=meng+wanzhou+site:www.nbcnews.com/",
                      "https://news.google.com/search?q=meng+wanzhou+site:www.foxnews.com/",
                      "https://news.google.com/search?q=meng+wanzhou+site:edition.cnn.com/",
                      "https://news.google.com/search?q=meng+wanzhou+site:www.npr.org/",
                      "https://news.google.com/search?q=meng+wanzhou+site:www.nytimes.com/",
                      ]
        splash_args = {
            'wait': 0.5,
        }
        for url in start_urls:
            # 包含yield语句的函数是一个生成器
            # 生成器每次产生一个值（yield语句），函数被冻结，被唤醒后再产生一个值，生成器是一个不断产生值的函数
            yield scrapy.Request(url=url, callback=self.parse_result, dont_filter=False)
            # yield SplashRequest(url, self.parse_result, endpoint='render.html',args=splash_args)

    def parse_result(self, response):
        item = MengEventItem()
        # item['originalPage'] = response.text

        newsLinks = response.xpath('//div[@class="NiLAwe y6IFtc R7GTQ keNKEd j7vNaf nID9nc"]/a/@href').extract()
        item['newsLinks'] = newsLinks

        yield item


    # TODO 这是一个获取页面链接的例子
    # def __init__(self, *args, **kwargs):
    #     super(baiduSpider, self).__init__(*args, **kwargs)
    #     self.start_urls = ['https://baike.baidu.com/item/李幼斌/12503']
    #
    # def parse(self, response):
    #     link = LinkExtractor(restrict_xpaths='//div[@id="slider_relations"]/ul/li/a')
    #     links = link.extract_links(response)
    #     if links:
    #         for link_one in links:
    #             print("relation_url:" + link_one.url + "\n" + "relation_name:" + link_one.text.strip())


    # TODO 这个是scrapy的另一个内置Spider，通过调用具体的spider
    # def start_requests(self):
    #     start_urls = ["https://baike.baidu.com/item/李幼斌/12504",
    #                   ]
    #     for url in start_urls:
    #         # 包含yield语句的函数是一个生成器
    #         # 生成器每次产生一个值（yield语句），函数被冻结，被唤醒后再产生一个值，生成器是一个不断产生值的函数
    #         yield scrapy.Request(url=url, callback=self.parse, dont_filter=False)
    #
    # def parse(self, response):
    #     pass
