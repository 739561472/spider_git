from scrapy import cmdline
cmdline.execute('scrapy crawl books -o books.csv'.split())