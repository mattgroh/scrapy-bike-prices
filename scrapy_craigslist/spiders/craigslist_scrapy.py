__author__ = 'anon'

from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.contrib.spiders import Rule, CrawlSpider
from scrapy.selector import Selector
from scrapy_craigslist.items import ScrapyCraigslistItem
from scrapy import Request

import re
from datetime import datetime
from bs4 import BeautifulSoup
import time
import random
from urls import urls


class MySpider(CrawlSpider):
    """
    This CrawlSpider will look into a list of cities (from https://sites.google.com/site/clsiteinfo/city-site-code-sort)
    and pull out content for each Craigslist Ad.
    """

    

    name = 'craigslist'
    section = 'bia'
    allowed_domains = []
    start_urls = []
    for i in urls:
        city = re.sub("http://","",i)
        start_urls.append('https://{0}/search/{1}?'.format(city,section))
        allowed_domains.append(city)

    rules = (
        Rule(LxmlLinkExtractor(
            allow=(r'.*/search/{0}.*'.format(section)),
            deny = (r'.*format\=rss.*')
        ),
            callback="parse_items_1",
            follow= True,
             ),
        )

    def parse_items_1(self, response):
        """
        This function finds all ad links for the last 24 hours and crawls those ads
        """
        r_rows = "//ul[@class='rows']/*"
        r_ad_urls = "//li/a/@href"
        re_posttime = "//li/p/time"

        self.logger.info('You are now crawling: %s', response.url)
        hxs = Selector(response)
        contents = hxs.xpath(r_rows)
        content = contents[0]
        rows = len(content.xpath(r_ad_urls).extract())
        city = re.sub('/search.*',"",re.sub('https://',"", response.url))        
        self.logger.info('\n\n' + city + '\n\n' + 'Looping through %s rows', rows)
        last24 = True
        while(last24==True):
            for i in range(0,rows):
                hours_since_post = (datetime.now() - datetime.strptime(re.sub('".*',"",re.sub('.*datetime="',"",content.xpath(re_posttime).extract()[i])), "%Y-%m-%d %H:%M")).seconds/(60*60)
                if hours_since_post > 24:
                    last24 = False
                else:
                    try:
                        k = content.xpath(r_ad_urls).extract()[i]
                        if ".html" in k:
                            yield Request('https://{0}{1}'.format(city, ''.join(k)),
                                         callback=self.parse_ad)
                    except IndexError:
                        self.logger.info('\n\n\n\n ERROR -- %s', "ad_url not found")
            last24 = False

    def parse_ad(self, response):
        """
        This function extracts specific data for each ad
        """
        item = ScrapyCraigslistItem()
        item ["url"] = response.url
        item ["post_id"] = re.sub("post id:", "", response.xpath("//section/section/div[@class='postinginfos']/p/text()").extract()[0])
        item ["city"] = response.xpath("//section/header/nav/ul/li/p/a/text()").extract()[0]
        item ["title"] = response.xpath("//section/h2//span/span[@id='titletextonly']/text()").extract()[0]
        try:
            item ["price"] = re.sub("[^0-9]","",response.xpath("//section/h2//span/span[@class='price']/text()").extract()[0])
        except IndexError:
            item ["price"] = ""
        item ["body"] = re.sub("\n"," ","".join(response.xpath("//section/section/section[@id='postingbody']/text()").extract())).strip()
        item ["post_time"] = response.xpath("//section/section/div[@class='postinginfos']/p/time/text()").extract()[0]
        try:
            item ["update_time"] = response.xpath("//section/section/div[@class='postinginfos']/p/time/text()").extract()[1]
        except IndexError:
            item ["update_time"] = response.xpath("//section/section/div[@class='postinginfos']/p/time/text()").extract()[0]
        try:
            geo = response.xpath("//section/section/div/div/div[@id='map']").extract()[0]
            soup = BeautifulSoup(geo)
            item ["lat"] = soup.find_all(attrs={"data-latitude": True, "data-longitude": True})[0]["data-latitude"]
            item ["lon"] = soup.find_all(attrs={"data-latitude": True, "data-longitude": True})[0]["data-longitude"]
        except:
            item ["lat"] = ""
            item ["lon"] = ""
        try:
            item ["make"] = response.xpath("//section/div/p/span/b/text()").extract()[1]
            item ["model"] = response.xpath("//section/div/p/span/b/text()").extract()[2]
        except IndexError:
            item ["make"] = ""
            item ["model"] = ""
        try:
            imageurls = response.xpath("//section/section//div/a/@href").extract()
            item["image_urls"] = imageurls
            for image_url in imageurls:
                yield Request(image_url)
        except:
            item["image_urls"] = []
            item ["images"] = []
        yield item

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item


