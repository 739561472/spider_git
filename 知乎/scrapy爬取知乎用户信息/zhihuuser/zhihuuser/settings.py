# -*- coding: utf-8 -*-

# Scrapy settings for zhihuuser project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'zhihuuser'

SPIDER_MODULES = ['zhihuuser.spiders']
NEWSPIDER_MODULE = 'zhihuuser.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'zhihuuser (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'accept': 'application/json, text/plain, */*',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
    'Connection': 'keep-alive',
    'Cookie': '_zap=0ad13437-1f6b-4d51-90e5-5fa9b3ee60ea; d_c0="AECCMCl-1wyPTj22u6rDh3P9kEgxFV88TZE=|1513399908"; q_c1=5ddb74d22f8249cf84ebbacd65f69333|1515327515000|1512543978000; aliyungf_tc=AQAAAEpMnz1D5QUAe9rWcetpEZ8e7W6v; _xsrf=c1e02c91-092d-47ba-901c-2e2f1b531180; l_cap_id="NDE2MjFmNTBkMGFlNGEzOGE5ZTMwMzZhODM4NjUyNWU=|1516693141|bbbf191ea8664198154fb787afd24237a013e6f5"; r_cap_id="MjU1M2IwYTk5NGMxNGI3MDg3YjhiMTc3NTkyMWFiYzg=|1516693141|d673cf2dcd9a4315cb08ae0b51707834dd51f115"; cap_id="NDUzNTkyNDA2NWU0NGIwNTkxN2ZhODdiYWNmNTY4ODk=|1516693141|e98bebc5f2cc0fe3f5936b75fe9507a9b3297cfb"; anc_cap_id=379df63bac7247faa82fe82938e6263e; __utma=155987696.1917672464.1516952113.1516952113.1516952113.1; __utmb=155987696.0.10.1516952113; __utmc=155987696; __utmz=155987696.1516952113.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); capsion_ticket="2|1:0|10:1516953495|14:capsion_ticket|44:MjY1OGU2Y2E4NzczNDMyMDlmNDY5Njg5OTdhZjQ5MDk=|40dcca0120344a823f749a08681add7619150ca829cce73ed480ceac4ea92f66"',
    'Host': 'www.zhihu.com',
    'Referer': 'https://www.zhihu.com/people/excited-vczh/following',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'X-UDID': 'AECCMCl-1wyPTj22u6rDh3P9kEgxFV88TZE=',
}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'zhihuuser.middlewares.ZhihuuserSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'zhihuuser.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'zhihuuser.pipelines.MongoDBPipeline': 300,
}
MONGO_URI = 'localhost:27017'
MONGO_DB = 'zhihu'
# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
