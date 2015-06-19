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