# -*- coding: utf-8 -*-

# Scrapy settings for whatpub_scrapy project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'whatpub_scrapy'

SPIDER_MODULES = ['whatpub_scrapy.spiders']
NEWSPIDER_MODULE = 'whatpub_scrapy.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'whatpub_scrapy (+http://www.yourdomain.com)'

DOWNLOAD_TIMEOUT = 360
AUTOTHROTTLE_ENABLED = True
