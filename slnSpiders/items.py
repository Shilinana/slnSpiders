# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GithubCatagaryItem(scrapy.Item):
    # name = scrapy.Field()
    catagary = scrapy.Field()
    language = scrapy.Field()
    start = scrapy.Field()
    fork = scrapy.Field()
    author = scrapy.Field()
    repo = scrapy.Field()