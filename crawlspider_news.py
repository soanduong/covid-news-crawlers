# -*- coding: utf-8 -*-
"""
Created on 22/02/2021 4:27 pm

@author: Soan Duong, UOW
"""
# Standard library imports
import numpy as np
from datetime import datetime

# Third party imports
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


# Local application imports
KEYWORDS = ['coronavirus', 'covid', 'ncov', 'sars-cov', 'viem phoi']
START_DATE = datetime(2019, 11, 17, 0, 0, 0)
END_DATE = datetime(2021, 2, 23, 0, 0, 0)


class CrawlSpider_vnexpress(CrawlSpider):
    name = 'vnexpress'
    allowed_domains = ['vnexpress.net']
    start_urls = ['https://vnexpress.net/']
    rules = [Rule(LinkExtractor(allow=['vnexpress.net/.+'],
                                deny_domains=['shop.vnexpress.net']),
                  callback='parse_article', follow=True)]

    def parse_article(self, response):
        print('Got a response from {}'.format(response.url))

        # Extract the source in case response.url is the url of the article
        art = response.xpath('//body[@data-source="Detail"]')
        if art:
            # Extract the published date
            art_date = art.xpath('//meta[@name="pubdate"]/@content')[0].get()
            art_date = datetime.fromisoformat(art_date).replace(tzinfo=None)
            print('Date: ', art_date)

            # Extract the article information if the published date is within the period of interest
            if START_DATE <= art_date and \
                    (END_DATE is None or END_DATE > art_date):
                # Extract the title of the article
                art_title = art.xpath('//title/text()').extract()[0]

                # Extract the keywords of the article
                art_keywords = art.xpath('//meta[@name="news_keywords"]/@content')[0].get()

                # Extract the description of the article
                art_description = art.xpath('//meta[@name="description"]/@content')[0].get()

                # Check if the interest keywords are in the title
                # or news keywords or description
                keyword_existed = (any(kw in art_title.lower() for kw in KEYWORDS) or
                                   any(kw in art_keywords.lower() for kw in KEYWORDS) or
                                   any(kw in art_description.lower() for kw in KEYWORDS))
                if keyword_existed:
                    print('Title: ', art_title)
                    yield {'date': art_date.strftime('%Y-%m-%d'),
                           'url': response.url,
                           'title': art_title,
                           'keywords': art_keywords,
                           'description': art_description,
                           'published_datetime': art_date}


# ------------------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    FILE_NAME = 'data/vnexpress.jsonl'
    SETTINGS = {'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
                'FEED_FORMAT': 'jsonlines',
                'FEED_URI': FILE_NAME,
                'CONCURRENT_ITEMS': 1}

    process = CrawlerProcess(SETTINGS)
    process.crawl(CrawlSpider_vnexpress)
    process.start()
    print('Done')