# -*- coding: utf-8 -*-
import re
import requests
from scrapy.spider import Spider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from urlparse import urlparse, urljoin
from scrapy.selector import Selector
from time import sleep
import urllib
from whatpub_scrapy.items import WhatpubScrapyItem
from scrapy.http import Request, FormRequest
from dateutil import rrule, parser
from dateutil import relativedelta
from datetime import timedelta, datetime
from scrapy.log import ScrapyFileLogObserver
from scrapy import log
from scrapy.shell import inspect_response
import time
import json

class WhatpubSpider(Spider):
    name = 'whatpub'
    start_urls = ['http://whatpub.com', ]
    allowed_domains = ['whatpub.com']
    TIMEZONE = ''
    BASE_URL = 'http://whatpub.com'

    def __init__(self, name=None, **kwargs):
        ScrapyFileLogObserver(open("spider.log", 'w'), level=log.INFO).start()
        ScrapyFileLogObserver(open("spider_error.log", 'w'), level=log.ERROR).start()
        super(WhatpubSpider, self).__init__(name, **kwargs)

    def parse(self, response):
        zip_file = open('ukpostcodes.txt', 'r+')
        zip_list = filter(None, list(set(zip_file.read().split('\n'))))
        for zip_item in zip_list:
            search_url = 'http://whatpub.com/search'
            params = {'q':'%s'%(zip_item),
                      't':'ft',
                      'p':'1',
                      'features':'Pub,RealAle,Open'}
            search_url = search_url+'?%s'%(urllib.urlencode(params))
            yield Request(url=search_url, callback=self.parse_venue_list, dont_filter=True)

    def parse_venue_list(self, response):
        sel = Selector(response)

        VENUE_LIST_XPATH = '//article[@class="pubs"]/section[@class="pub"]/a/@href'

        venue_list = sel.xpath(VENUE_LIST_XPATH).extract()
        if venue_list:
            for venue_item in venue_list:
                venue_item = venue_item if venue_item.startswith('http') else self.BASE_URL+venue_item
                yield Request(url=venue_item, callback=self.parse_venue)
        else:
            return

        NEXT_URL_XPATH = '//a[@title="More"]/@href'
        next_url = sel.xpath(NEXT_URL_XPATH).extract()
        next_url = self.BASE_URL+next_url[0] if next_url else ''
        if next_url:
            yield Request(url=next_url, callback=self.parse_venue_list, dont_filter=True)

    def parse_venues(self, response):
        item = WhatpubScrapyItem(venue_url = response.url)
        yield item

    def parse_venue(self, response):
        sel = Selector(response)

        PUB_ID_XPATH = '//article[@id="pub"]/@data-id'

        get_pub_info_url = 'http://whatpub.com/api/1/GetPubDetails'
        pub_id = sel.xpath(PUB_ID_XPATH).extract()
        pub_id = pub_id[0] if pub_id else ''
        params = {'PubID':pub_id}
        pub_response = requests.post(url=get_pub_info_url, data=params)
        json_data = json.loads(pub_response.content)

        json_response = json_data.get('response', {})
        address = ', '.join(filter(None,[json_response.get('Street', ''), json_response.get('District', ''), json_response.get('Town', ''), json_response.get('Posttown', ''), json_response.get('Postcode', '')]))
        website = json_response.get('Website', '')
        venue_name = json_response.get('Name', '')
        venue_url = response.url

        item = WhatpubScrapyItem(address = address,
                                 website = website,
                                 venue_name = venue_name,
                                 venue_url = venue_url)
        yield item