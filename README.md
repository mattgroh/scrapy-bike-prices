Crawling Bicycle Prices on Craigslist
===========

## Terms of Service

Please read Craigslist's Terms of Service before attempting to crawl its webpages. This script is simply intended to show it's possible but not to scrape or crawl ;)

## Why Crawl Bicycle Prices

Aggregate data can tell fascinating stories. Craigslist is the most frequently used marketplace for bicycles, which makes it a great source on understanding used bicycle markets. I'm curious what how the bicycle prices, bicycle styles (road/hybrid/mountain/fixed gear), and the availability of rare, classic bicycles vary across cities. Theoretically, is bicycle arbitrage possible? What makes for a high quality ad? What bicycles stay on the market for a long time? Is it possible to automatically identify great deals or ripoffs? 

## Handling Shifting Structure

You may need to handle a shifting url structure from a website you crawl, so you'll want to use scrapy shell to test out your new parsers.

`scrapy shell url`

## Let's Crawl

If you want to test the crawl locally, run scrapy

`scrapy crawl craigslist -o output.json`

In order to avoid getting blocked by the websites you are crawling, you'll want to rotate the IP addresses that you use to access the website. Scraping Hub is a great service that provides an API to do this for free. Go to [Scrapinghub](https://doc.scrapinghub.com/shub.html) to learn more.  

```
pip install shub
shub login
```

Add your credentials and S3 bucket

``` 
cd scrapy_craigslist
echo creds={\"aws_id\":\"xx\", \"aws_secret\":\"xx\", \"s3\":\"s3_bucket_url\"} >> creds.py
cd ..
```

```
shub deploy
shub schedule craigslist
shub items [crawl_id]
```

## User Agent

Check out [useragent.io](http://api.useragent.io/) if you want to generate a new user agent
for your crawl job.

