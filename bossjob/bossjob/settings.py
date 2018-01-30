# -*- coding: utf-8 -*-

# Scrapy settings for bossjob project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'bossjob'

SPIDER_MODULES = ['bossjob.spiders']
NEWSPIDER_MODULE = 'bossjob.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'bossjob (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Encoding': 'gzip, deflate, br',
  'Accept-Language': 'en',
  'Connection': 'keep-alive',
  'Cookie': '__c=1517110196; sid=sem_pz_bdpc_index; JSESSIONID=""; __g=sem_pz_bdpc_index; t=iGcQPXyIjhJJIhxs; wt=iGcQPXyIjhJJIhxs; __l=r=http%3A%2F%2Fbzclk.baidu.com%2Fadrc.php%3Ft%3D06KL00c00fDNJKT0L27U0KZEgsAzfvdp000005DIW-b00000uRT-Jj.THdBULP1doZA80K85yF9pywd0ZnqmWPBP16Lnvcsnj0kuAuWP6Kd5H64nj-DfRn3wDnvwWDkPYnzfHD3PbNjwDc4PW6vwWmL0ADqI1YhUyPGujY1nj6krj64nHnkFMKzUvwGujYkP6K-5y9YIZK1rBtEILILQMGCpgKGUB4WUvYE5LPGujd1uydxTZGxmhwsmdqGUhw-X0KWThnqnHfsPWf%26tpl%3Dtpl_10085_16624_12226%26l%3D1502486001%26attach%3Dlocation%253D%2526linkName%253D%2525E6%2525A0%252587%2525E9%2525A2%252598%2526linkText%253DBOSS%2525E7%25259B%2525B4%2525E8%252581%252598%2525EF%2525BC%25259A%2525E6%25258D%2525A2%2525E5%2525B7%2525A5%2525E4%2525BD%25259C%2525E5%2525B0%2525B1%2525E6%252598%2525AF%2525E6%25258D%2525A2Boss%2526xp%253Did(%252522m1a963c03%252522)%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FH2%25255B1%25255D%25252FA%25255B1%25255D%2526linkType%253D%2526checksum%253D105%26ie%3Dutf-8%26f%3D3%26tn%3Dbaidu%26wd%3Dboss%25E7%259B%25B4%25E8%2581%2598%26oq%3D51job%2525E5%252592%25258C%2525E6%25258B%252589%2525E5%25258B%2525BE%26rqlang%3Dcn%26inputT%3D5024%26prefixsug%3DBOss%26rsp%3D2&l=%2F%3Fsid%3Dsem_pz_bdpc_index%22&g=%2Fwww.zhipin.com%2F%3Fsid%3Dsem_pz_bdpc_index; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1517110197,1517112513; lastCity=101210100; __a=34772647.1517110196.1517111232.1517110196.44.3.20.44; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1517114327',
  'Host': 'www.zhipin.com',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'bossjob.middlewares.BossjobSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'bossjob.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'bossjob.pipelines.MongoDBPipeline': 400,
}
MONGO_URI = 'localhost'
MONGO_DB = 'boss_jobs'

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
