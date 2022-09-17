#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 获取新闻内容
Desc :
"""

from scrapy.spider import CrawlSpider,Rule
from mengEventProject.items import ArticleItem

class ArticleSpider(CrawlSpider):
    name = "acticleSpider"

    def __init__(self,rule):
        self.rule = rule
        self.name = rule.name
        self.allowed_domains = rule.allowed_domains.split(",")
        self.start_urls = rule.start_urls.split(",")

        super(ArticleSpider, self).__init__()

    def parse_item(self, response):
        self.log('this is an article page %s' % response.url)

        article = ArticleItem()
        article["url"] = response.url

        title = response.xpath(self .rule.title_xpath).extract()
        article['title'] = title

        body = response.xpath(self.rule.body_xpath).extract()
        article["body"] = body

        return article

