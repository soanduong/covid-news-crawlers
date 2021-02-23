# -*- coding: utf-8 -*-
"""
Created on 22/02/2021 4:27 pm

@author: Soan Duong, UOW
"""
# Standard library imports
import json
import argparse
import numpy as np
from datetime import datetime

# Third party imports
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


KEYWORDS = ['coronavirus', 'corona virus', 'covid', 'ncov', 'sars-cov', 'viem phoi']
START_DATE = datetime(2019, 11, 17, 0, 0, 0)
END_DATE = datetime(2021, 2, 23, 0, 0, 0)


def exist_keywords(content):
    return any(kw in content.lower() for kw in KEYWORDS)


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
            print('Published date: ', art_date)

            # Extract the article information if the published date is within the period of interest
            if START_DATE <= art_date and \
                    (END_DATE is None or END_DATE > art_date):
                art_title = ''
                art_keywords = ''
                art_description = ''
                try:
                    # Extract the title of the article
                    art_title = art.xpath('//title/text()').extract()[0]

                    # Extract the keywords of the article
                    art_keywords = art.xpath('//meta[@name="news_keywords"]/@content')[0].get()

                    # Extract the description of the article
                    art_description = art.xpath('//meta[@name="description"]/@content')[0].get()
                except:
                    print('Error in extracting the content')
                # Check if the interest keywords are in the title
                # or news keywords or description
                if exist_keywords(art_title + art_keywords + art_description):
                    print('Title: ', art_title)
                    yield {'date': art_date.strftime('%Y-%m-%d'),
                           'url': response.url,
                           'title': art_title,
                           'keywords': art_keywords,
                           'description': art_description,
                           'published_datetime': art_date}


class CrawlSpider_laodong(CrawlSpider):
    name = 'laodong'
    allowed_domains = ['laodong.vn']
    start_urls = ['https://laodong.vn/']
    rules = [Rule(LinkExtractor(allow=['laodong.vn/.+'],
                                deny=['laodong.vn/video/.+']),
                  callback='parse_article', follow=True)]

    def parse_article(self, response):
        print('Got a response from {}'.format(response.url))

        # Extract the source in case response.url is the url of the article
        art = response.xpath('//body[@class="article-n2"]')
        if not art:
            art = response.xpath('//body[@class="article-m2"]')
        if art:
            # Extract the published date
            art_date = art.xpath('//time[@class="f-datetime"]/text()').extract()[0]
            art_date = datetime.strptime(art_date, "%d/%m/%Y | %H:%M")
            print('Published date: ', art_date)

            # Extract the article information if the published date is within the period of interest
            if START_DATE <= art_date and \
                    (END_DATE is None or END_DATE > art_date):
                art_title = ''
                art_keywords = ''
                art_description = ''
                try:
                    # Extract the title of the article
                    art_title = art.xpath('//title/text()').extract()[0]

                    # Extract the keywords of the article
                    art_keywords = art.xpath('//meta[@name="keywords"]/@content')[0].get()

                    # Extract the description of the article
                    art_description = art.xpath('//meta[@name="description"]/@content')[0].get()
                except:
                    print('Error in extracting the content')

                # Check if the interest keywords are in the title
                # or news keywords or description
                if exist_keywords(art_title + art_keywords + art_description):
                    print('Title: ', art_title)
                    yield {'date': art_date.strftime('%Y-%m-%d'),
                           'url': response.url,
                           'title': art_title,
                           'keywords': art_keywords,
                           'description': art_description,
                           'published_datetime': art_date}


class CrawlSpider_vtv(CrawlSpider):
    name = 'vtv'
    allowed_domains = ['vtv.vn']
    start_urls = ['https://vtv.vn/']
    rules = [Rule(LinkExtractor(allow=['vtv.vn/.+'],
                                deny=['vtv.vn/video/.+']),
                  callback='parse_article', follow=True)]

    def parse_article(self, response):
        print('Got a response from {}'.format(response.url))

        # Extract the source in case response.url is the url of the article
        art = response.xpath('//meta[@property="article:section"]')
        if art:
            # Extract the published date
            art_date = art.xpath('//meta[@name="pubdate"]/@content')[0].get()
            art_date = datetime.fromisoformat(art_date).replace(tzinfo=None)
            print('Published date: ', art_date)

            # Extract the article information if the published date is within the period of interest
            if START_DATE <= art_date and \
                    (END_DATE is None or END_DATE > art_date):
                art_title = ''
                art_keywords = ''
                art_description = ''
                try:
                # Extract the title of the article
                    art_title = art.xpath('//title/text()').extract()[0]

                    # Extract the keywords of the article
                    art_keywords = art.xpath('//meta[@name="news_keywords"]/@content')[0].get()

                    # Extract the description of the article
                    art_description = art.xpath('//meta[@name="description"]/@content')[0].get()
                except:
                    print('Error in extracting the content')

                # Check if the interest keywords are in the title
                # or news keywords or description
                if exist_keywords(art_title + art_keywords + art_description):
                    print('Title: ', art_title)
                    yield {'date': art_date.strftime('%Y-%m-%d'),
                           'url': response.url,
                           'title': art_title,
                           'keywords': art_keywords,
                           'description': art_description,
                           'published_datetime': art_date}


class CrawlSpider_24h(CrawlSpider):
    name = '24h'
    allowed_domains = ['24h.com.vn']
    start_urls = ['https://24h.com.vn/']
    rules = [Rule(LinkExtractor(allow=['24h.com.vn/.+.html'],
                                deny=['24h.com.vn/video-.+']),
                  callback='parse_article', follow=True)]

    def parse_article(self, response):
        print('Got a response from {}'.format(response.url))

        # Extract the source in case response.url is the url of the article
        art = response.xpath('//div[@class="brmCm2 brmCm2x"]')
        if art and len(response.url.split(('/'))) > 4:
            # Extract the published date
            art_date = art.xpath('//meta[@name="pubdate"]/@content')[0].get()
            art_date = datetime.fromisoformat(art_date).replace(tzinfo=None)
            print('Published date: ', art_date)

            # Extract the article information if the published date is within the period of interest
            if START_DATE <= art_date and \
                    (END_DATE is None or END_DATE > art_date):
                art_title = ''
                art_keywords = ''
                art_description = ''
                try:
                # Extract the title of the article
                    art_title = art.xpath('//title/text()').extract()[0]

                    # Extract the keywords of the article
                    art_keywords = art.xpath('//meta[@name="news_keywords"]/@content')[0].get()

                    # Extract the description of the article
                    art_description = art.xpath('//meta[@name="description"]/@content')[0].get()
                except:
                    print('Error in extracting the content')

                # Check if the interest keywords are in the title
                # or news keywords or description
                if exist_keywords(art_title + art_keywords + art_description):
                    print('Title: ', art_title)
                    yield {'date': art_date.strftime('%Y-%m-%d'),
                           'url': response.url,
                           'title': art_title,
                           'keywords': art_keywords,
                           'description': art_description,
                           'published_datetime': art_date}


class CrawlSpider_zingnews(CrawlSpider):
    name = 'zingnews'
    allowed_domains = ['zingnews.vn']
    start_urls = ['https://zingnews.vn/']
    rules = [Rule(LinkExtractor(allow=['zingnews.vn/.+']),
                  callback='parse_article', follow=True)]

    def parse_article(self, response):
        print('Got a response from {}'.format(response.url))

        # Extract the source in case response.url is the url of the article
        art = response.xpath('//body[@id="page-article"]')
        if art:
            # Extract the published date
            art_date = art.xpath('//meta[@property="article:published_time"]/@content')[0].get()
            art_date = datetime.strptime(art_date, "%Y-%m-%dT%H:%M:%S%z").replace(tzinfo=None)
            print('Published date: ', art_date)

            # Extract the article information if the published date is within the period of interest
            if START_DATE <= art_date and \
                    (END_DATE is None or END_DATE > art_date):
                art_title = ''
                art_keywords = ''
                art_description = ''
                try:
                    # Extract the title of the article
                    art_title = art.xpath('//title/text()').extract()[0]

                    # Extract the keywords of the article
                    art_keywords = art.xpath('//meta[@name="keywords"]/@content')[0].get()

                    # Extract the description of the article
                    art_description = art.xpath('//meta[@name="description"]/@content')[0].get()
                except:
                    print('Error in extracting the content')

                # Check if the interest keywords are in the title
                # or news keywords or description
                if exist_keywords(art_title + art_keywords + art_description):
                    print('Title: ', art_title)
                    yield {'date': art_date.strftime('%Y-%m-%d'),
                           'url': response.url,
                           'title': art_title,
                           'keywords': art_keywords,
                           'description': art_description,
                           'published_datetime': art_date}


class CrawlSpider_kenh14(CrawlSpider):
    name = 'kenh14'
    allowed_domains = ['kenh14.vn']
    start_urls = ['https://kenh14.vn/']
    rules = [Rule(LinkExtractor(allow=['kenh14.vn/.+'],
                                deny_domains=['video.kenh14.vn']),
                  callback='parse_article', follow=True)]

    def parse_article(self, response):
        print('Got a response from {}'.format(response.url))

        # Extract the source in case response.url is the url of the article
        art = response.xpath('//div[@class="knc-content"]')
        if art:
            # Extract the published date
            art_date = art.xpath('//meta[@property="article:published_time"]/@content')[0].get()
            art_date = datetime.fromisoformat(art_date).replace(tzinfo=None)
            print('Published date: ', art_date)

            # Extract the article information if the published date is within the period of interest
            if START_DATE <= art_date and \
                    (END_DATE is None or END_DATE > art_date):
                art_title = ''
                art_keywords = ''
                art_description = ''
                try:
                    # Extract the title of the article
                    art_title = art.xpath('//title/text()').extract()[0]

                    # Extract the keywords of the article
                    art_keywords = art.xpath('//meta[@name="news_keywords"]/@content')[0].get()

                    # Extract the description of the article
                    art_description = art.xpath('//meta[@name="description"]/@content')[0].get()
                except:
                    print('Error in extracting the content')

                # Check if the interest keywords are in the title
                # or news keywords or description
                if exist_keywords(art_title + art_keywords + art_description):
                    print('Title: ', art_title)
                    yield {'date': art_date.strftime('%Y-%m-%d'),
                           'url': response.url,
                           'title': art_title,
                           'keywords': art_keywords,
                           'description': art_description,
                           'published_datetime': art_date}


class CrawlSpider_dantri(CrawlSpider):
    name = 'dantri'
    allowed_domains = ['dantri.com.vn']
    start_urls = ['https://dantri.com.vn/']
    rules = [Rule(LinkExtractor(allow=['dantri.com.vn/.+'],
                                deny=['dantri.com.vn/video.']),
                  callback='parse_article', follow=True)]

    def parse_article(self, response):
        print('Got a response from {}'.format(response.url))

        # Extract the source in case response.url is the url of the article
        art = response.xpath('//body[@data-isrc="articlev2"]')
        if art:
            # Extract the published date
            scripts = art.xpath('//script[@type="application/ld+json"]/text()')
            for script in scripts:
                script = json.loads(script.get())
                if 'datePublished' in script:
                    art_date = script['datePublished']
                    break
            if '.' not in art_date:
                art_date = art_date + '.'
            art_date = datetime.fromisoformat(art_date.ljust(23, '0')).replace(tzinfo=None)
            print('Published date: ', art_date)

            # Extract the article information if the published date is within the period of interest
            if START_DATE <= art_date and \
                    (END_DATE is None or END_DATE > art_date):
                art_title = ''
                art_keywords = ''
                art_description = ''
                try:
                    # Extract the title of the article
                    art_title = art.xpath('//meta[@name="title"]/@content')[0].get()

                    # Extract the keywords of the article
                    art_keywords = art.xpath('//meta[@name="keywords"]/@content')[0].get()

                    # Extract the description of the article
                    art_description = art.xpath('//meta[@name="description"]/@content')[0].get()
                except:
                    print('Error in extracting the content')

                # Check if the interest keywords are in the title
                # or news keywords or description
                if exist_keywords(art_title + art_keywords + art_description):
                    print('Title: ', art_title)
                    yield {'date': art_date.strftime('%Y-%m-%d'),
                           'url': response.url,
                           'title': art_title,
                           'keywords': art_keywords,
                           'description': art_description,
                           'published_datetime': art_date}


class CrawlSpider_tuoitre(CrawlSpider):
    name = 'tuoitre'
    allowed_domains = ['tuoitre.vn']
    start_urls = ['https://tuoitre.vn/']
    rules = [Rule(LinkExtractor(allow=['tuoitre.vn/.+'],
                                deny_domains=['tv.tuoitre.vn']),
                  callback='parse_article', follow=True)]

    def parse_article(self, response):
        print('Got a response from {}'.format(response.url))

        # Extract the source in case response.url is the url of the article
        art = response.xpath('//meta[@property="article:section"]')
        if art:
            # Extract the published date
            art_date = art.xpath('//meta[@property="article:published_time"]/@content')[0].get()
            art_date = datetime.fromisoformat(art_date).replace(tzinfo=None)
            print('Published date: ', art_date)

            # Extract the article information if the published date is within the period of interest
            if START_DATE <= art_date and \
                    (END_DATE is None or END_DATE > art_date):
                art_title = ''
                art_keywords = ''
                art_description = ''
                try:
                    # Extract the title of the article
                    art_title = art.xpath('//meta[@property="og:title"]/@content')[0].get()

                    # Extract the keywords of the article
                    art_keywords = art.xpath('//meta[@name="keywords"]/@content')[0].get()

                    # Extract the description of the article
                    art_description = art.xpath('//meta[@name="description"]/@content')[0].get()
                except:
                    print('Error in extracting the content')

                # Check if the interest keywords are in the title
                # or news keywords or description
                if exist_keywords(art_title + art_keywords + art_description):
                    print('Title: ', art_title)
                    yield {'date': art_date.strftime('%Y-%m-%d'),
                           'url': response.url,
                           'title': art_title,
                           'keywords': art_keywords,
                           'description': art_description,
                           'published_datetime': art_date}


class CrawlSpider_vietnamnet(CrawlSpider):
    name = 'vietnamnet'
    allowed_domains = ['vietnamnet.vn']
    start_urls = ['https://vietnamnet.vn/']
    rules = [Rule(LinkExtractor(allow=['vietnamnet.vn/.+'],
                                deny=['vietnamnet.vn/vn/talkshow/.']),
                  callback='parse_article', follow=True)]

    def parse_article(self, response):
        print('Got a response from {}'.format(response.url))

        # Extract the source in case response.url is the url of the article
        art = response.xpath('//body')
        scripts = art.xpath('//script[@type="application/ld+json"]/text()')
        if art and len(scripts) > 1:
            # Extract the published date
            for script in scripts:
                script = json.loads(script.get())
                if 'datePublished' in script:
                    art_date = script['datePublished']
                    break
            art_date = datetime.fromisoformat(art_date).replace(tzinfo=None)
            print('Published date: ', art_date)

            # Extract the article information if the published date is within the period of interest
            if START_DATE <= art_date and \
                    (END_DATE is None or END_DATE > art_date):
                art_title = ''
                art_keywords = ''
                art_description = ''
                try:
                    # Extract the title of the article
                    art_title = art.xpath('//title/text()').extract()[0]

                    # Extract the keywords of the article
                    art_keywords = art.xpath('//meta[@name="news_keywords"]/@content')[0].get()

                    # Extract the description of the article
                    art_description = art.xpath('//meta[@name="description"]/@content')[0].get()
                except:
                    print('Error in extracting the content')

                # Check if the interest keywords are in the title
                # or news keywords or description
                if exist_keywords(art_title + art_keywords + art_description):
                    print('Title: ', art_title)
                    yield {'date': art_date.strftime('%Y-%m-%d'),
                           'url': response.url,
                           'title': art_title,
                           'keywords': art_keywords,
                           'description': art_description,
                           'published_datetime': art_date}


class CrawlSpider_cafef(CrawlSpider):
    name = 'cafef'
    allowed_domains = ['cafef.vn']
    start_urls = ['https://cafef.vn/']
    rules = [Rule(LinkExtractor(allow=['cafef.vn/.+']),
                  callback='parse_article', follow=True)]

    def parse_article(self, response):
        print('Got a response from {}'.format(response.url))

        # Extract the source in case response.url is the url of the article
        art = response.xpath('//meta[@property="article:section"]')
        if art:
            # Extract the published date
            scripts = art.xpath('//script[@type="application/ld+json"]/text()')
            for script in scripts:
                script = json.loads(script.get())
                if 'datePublished' in script:
                    art_date = script['datePublished']
                    break
            if '.' not in art_date:
                art_date = art_date + '.'
            art_date = datetime.fromisoformat(art_date.ljust(23, '0')).replace(tzinfo=None)
            print('Published date: ', art_date)

            # Extract the article information if the published date is within the period of interest
            if START_DATE <= art_date and \
                    (END_DATE is None or END_DATE > art_date):
                art_title = ''
                art_keywords = ''
                art_description = ''
                try:
                    # Extract the title of the article
                    art_title = art.xpath('//title/text()').extract()[0]

                    # Extract the keywords of the article
                    art_keywords = art.xpath('//meta[@name="news_keywords"]/@content')[0].get()

                    # Extract the description of the article
                    art_description = art.xpath('//meta[@name="description"]/@content')[0].get()
                except:
                    print('Error in extracting the content')

                # Check if the interest keywords are in the title
                # or news keywords or description
                if exist_keywords(art_title + art_keywords + art_description):
                    print('Title: ', art_title)
                    yield {'date': art_date.strftime('%Y-%m-%d'),
                           'url': response.url,
                           'title': art_title,
                           'keywords': art_keywords,
                           'description': art_description,
                           'published_datetime': art_date}


CRAWLERs = {'vnexpress': CrawlSpider_vnexpress,
            'laodong': CrawlSpider_laodong,
            'vtv': CrawlSpider_vtv,
            '24h': CrawlSpider_24h,
            'zingnews': CrawlSpider_zingnews,
            'kenh14': CrawlSpider_kenh14,
            'dantri': CrawlSpider_dantri,
            'tuoitre': CrawlSpider_tuoitre,
            'vietnamnet': CrawlSpider_vietnamnet,
            'cafef': CrawlSpider_cafef}
# ------------------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    args = argparse.ArgumentParser(description='Main file')
    args.add_argument('--site_name', default='kenh14', type=str,
                      help='Name of the online newspaper, e.g. vnexpress and laodong.')
    args.add_argument('--out_dir', default=None, type=str,
                      help='Directory for saving the output jsonlines file')
    cmd_args = args.parse_args()

    assert cmd_args.site_name is not None, "Please specify the name of the online newspaper"
    if cmd_args.out_dir is None:
        cmd_args.out_dir = 'data/'
    # Set the output filename
    FILE_NAME = '{}/{}.jsonl'.format(cmd_args.out_dir, cmd_args.site_name)
    SETTINGS = {'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
                'FEED_FORMAT': 'jsonlines',
                'FEED_URI': FILE_NAME,
                'CONCURRENT_ITEMS': 1}

    process = CrawlerProcess(SETTINGS)
    process.crawl(CRAWLERs[cmd_args.site_name])
    process.start()
    print('Done')