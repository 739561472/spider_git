# -*- coding: utf-8 -*-

# Scrapy settings for job51 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'job51'

SPIDER_MODULES = ['job51.spiders']
NEWSPIDER_MODULE = 'job51.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'job51 (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
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
  'Accept-Language': 'zh-CN,zh;q=0.9',
  'Cache-Control': 'max-age=0',
  'Connection': 'keep-alive',
  'Cookie': 'guid=15138227727131230097; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; _ujz=MTMzMTExNTA1MA%3D%3D; ps=us%3DW2JWPANlAioCYQFuVTZQfVBqBzJbcwVhUGJQfgA7VWBbYlA9B2IKOlQ9AGoBYVxrVGIHPgM3UHldDlU%252BXDEPXFs3%26%7C%26needv%3D0; 51job=cuid%3D133111505%26%7C%26cusername%3Dphone_18512446195%26%7C%26cpassword%3D%26%7C%26cname%3D%25BA%25CE%25CC%25EC%25BB%25AA%26%7C%26cemail%3D735951472%2540qq.com%26%7C%26cemailstatus%3D0%26%7C%26cnickname%3D%26%7C%26ccry%3D.0Pn6Ucu0pauk%26%7C%26cconfirmkey%3D73nFv3nL.%252FpFY%26%7C%26cresumeids%3D.0kQW3aBMYOzI%257C%26%7C%26cautologin%3D1%26%7C%26cenglish%3D0%26%7C%26sex%3D0%26%7C%26cnamekey%3D7375HWEbzvCpY%26%7C%26to%3DWWACagZnBTJdPQtmBmZXZAQyC3ZTJVtmB25cYA5hAV4AOVs4UzQGMVIxDGQKa11oUWNWblBjUntTZFUyWmRUbFliAmkGYAU1XTkLYw%253D%253D%26%7C%26; adv=adsnew%3D1%26%7C%26adsresume%3D1%26%7C%26adsfrom%3Dhttps%253A%252F%252Fwww.baidu.com%252Fbaidu.php%253Fsc.K600000-SwTdAzCGTyNc7HyAm6-q-_Na6GLCa6pzAsY4sL7TgwUHCiwT074AKwSJ0hzUG8xqFy_1_wbLu52ZeDsqYN-HNQf-cMcxAWw7PJNE7e5cDZeyeo0jo42SWsDaHw91Qf8bidDBjm666H05II3nsqOSLaXON82IDe5dJ4GGZXUV3f.DY_iRFhmRSylE2lqD7auh75ELu8WBspy2errOI__l_4TUj5eOS8zZ4rSWqXiEISEQO_qjrMXOqXMtEYgOWEzOqWO6xeNZSwOs5qo6E3O-_OgboJ9YY2PLl-ZKOcYUSZSwSLuq7OlhS2OwExOv5vl5UIOkUtMtHtI1oEd23O1u54ABOFuEOeAMl3O4ZeOO7NOcqojZgVm_HbzgqrizeuvF8ootIMAkMkLndSrieuovgLJpMpRt85R_nYQZubzU_B6.U1Yk0ZDqkejPE_eXYtT0TA-W5HD0IjLrLV5Z0A-V5HczPfKM5yF-TZnk0ZNG5yF9pywd0ZKGujY1n6KWpyfqnW6s0AdY5HDsnHPxnH0kPdtknjD4g1DsPjwxn1msnfKopHYs0ZFY5Hcdn0K-pyfqnWRvPj7xnHfdn-tznHDzndtkrjRdrNtznjb1n0KBpHYznjf0UynqnHcsPHmkn1cvg1TkP1fknHckndtLnHT4n1cLP1-xnH0zg100TgKGujYs0Z7Wpyfqn0KzuLw9u1Ys0A7B5HKxn0K-ThTqn0KsTjYzPjb4rHDdnHDk0A4vTjYsQW0snj0snj0s0AdYTjYs0AwbUL0qn0KzpWYs0Aw-IWdsmsKhIjYs0ZKC5H00ULnqn0KBI1Ykn0K8IjYs0ZPl5fKYIgnqP1csnH01PWRvnHTvnHTYnHR1P6Kzug7Y5HDdnHTsnW6Yn10snjR0Tv-b5y79PyczPWI9nj0sn16sPyf0mLPV5HujrRFAfRcvnWFjrDn3nHc0mynqnfKYIgfqnfKsUWYs0Z7VIjYs0Z7VT1Ys0ZGY5H00UyPxuMFEUHYsg1Kxn7tknjfvg100uA78IyF-gLK_my4GuZnqn7tsg1Kxn1DLrjD4g100TA7Ygvu_myTqn0Kbmv-b5H00ugwGujYVnfK9TLKWm1Ys0ZNspy4Wm1Ys0Z7VuWYs0AuWIgfqn0KhXh6qn0Khmgfqn0KlTAkdT1Ys0A7buhk9u1Y30Akhm1Ys0APzm1YznHRvrf%2526ck%253D5565.1.61.409.149.413.156.378%2526shh%253Dwww.baidu.com%2526sht%253Dbaiduhome_pg%2526us%253D1.0.1.0.0.0.0%2526ie%253Dutf-8%2526f%253D8%2526tn%253Dbaiduhome_pg%2526wd%253D%2525E5%252589%25258D%2525E9%252580%252594%2525E6%252597%2525A0%2525E5%2525BF%2525A7%2526oq%253D%2525E5%252589%25258D%2525E9%252580%252594%2525E6%252597%2525A0%2525E5%2525BF%2525A7%2526rqlang%253Dcn%2526usm%253D3%2526cq%253D%2525E6%252599%2525BA%2525E8%252581%252594%2525E6%25258B%25259B%2525E8%252581%252598%2526srcid%253D28310%2526rt%253D%2525E8%252581%25258C%2525E4%2525B8%25259A%2525E6%25258B%25259B%2525E8%252581%252598%2525E7%2525B1%2525BB%2525E7%2525BD%252591%2525E7%2525AB%252599%2526recid%253D21102%2526euri%253Dbce561c8d217488980daa22fb18b074c%2526bc%253D110101%26%7C%26adsnum%3D1039580; slife=resumeguide%3D1%26%7C%26lowbrowser%3Dnot%26%7C%26lastlogindate%3D20180127%26%7C%26; NSC_tfbsdi.51kpc.dpn-159=ffffffffc3a01b2145525d5f4f58455e445a4a423660; search=jobarea%7E%60020000%2C080200%7C%21ord_field%7E%600%7C%21recentSearch0%7E%601%A1%FB%A1%FA020000%2C080200%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0100%2C2500%A1%FB%A1%FA32%2C01%2C38%2C40%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA2%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1517028527%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA%7C%21recentSearch1%7E%601%A1%FB%A1%FA020000%2C080200%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FApython+%A1%FB%A1%FA2%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1517028771%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA%7C%21recentSearch2%7E%601%A1%FB%A1%FA020000%2C080200%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA32%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA2%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1517028471%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA%7C%21recentSearch3%7E%601%A1%FB%A1%FA020000%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA32%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA2%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1517028450%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA%7C%21recentSearch4%7E%601%A1%FB%A1%FA020000%2C080200%2C040000%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FAPython+%C5%C0%B3%E6%A1%FB%A1%FA2%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1516769265%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA%7C%21collapse_expansion%7E%601%7C%21',
  'Host': 'search.51job.com',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'job51.middlewares.Job51SpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'job51.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html

MONGO_URI = 'localhost'
MONGO_DB = '51job'

ITEM_PIPELINES = {
    'job51.pipelines.Job51Pipeline': 300,
    'job51.pipelines.MongoDBPipeline': 400
}

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
