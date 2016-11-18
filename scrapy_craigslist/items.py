# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyCraigslistItem(scrapy.Item):
    post_id = scrapy.Field()
    title = scrapy.Field()
    city = scrapy.Field()
    body = scrapy.Field()
    post_time = scrapy.Field()
    update_time = scrapy.Field()
    price = scrapy.Field()
    lat = scrapy.Field()
    lon = scrapy.Field()
    url = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    make = scrapy.Field()
    model = scrapy.Field()
