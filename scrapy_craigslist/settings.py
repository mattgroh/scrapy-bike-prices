# -*- coding: utf-8 -*-

# Scrapy settings for scrapy_craigslist project
from creds import creds
BOT_NAME = 'scrapy_craigslist'

SPIDER_MODULES = ['scrapy_craigslist.spiders']
NEWSPIDER_MODULE = 'scrapy_craigslist.spiders'

# DUPEFILTER_DEBUG = True

# DUPEFILTER_CLASS = 'scrapy_craigslist.filters.NoDuplicateUrl'

ITEM_PIPELINES = {
    'scrapy_craigslist.pipelines.DuplicatesPipeline': 10,
	'scrapy.pipelines.images.ImagesPipeline': 1,
}

IMAGES_STORE = creds["s3"]

IMAGES_MIN_HEIGHT = 125
IMAGES_MIN_WIDTH = 125

IMAGES_THUMBS = {
    'thumb': (125, 125),
}

IMAGES_EXPIRES = 180     

AWS_ACCESS_KEY_ID = creds["aws_id"]
AWS_SECRET_ACCESS_KEY = creds["aws_secret"]


USER_AGENT = "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.3a1pre) Gecko/20091118 Minefield/3.7a1pre (.NET CLR 3.5.30729)"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrapy_craigslist (+http://www.yourdomain.com)'
