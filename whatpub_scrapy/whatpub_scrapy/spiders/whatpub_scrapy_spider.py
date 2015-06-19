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