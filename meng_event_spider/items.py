# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MengEventItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    originalPage = scrapy.Field()
    newsLinks = scrapy.Field()
    id = scrapy.Field()

class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    author = scrapy.Field()
    body = scrapy.Field()
    publish_time = scrapy.Field()
