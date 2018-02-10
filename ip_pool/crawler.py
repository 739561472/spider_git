import re
from time import sleep

from utils import get_page
from lxml import etree


class ProxyMetaclass(type):
    # 元类
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class ProxyCrawler(object, metaclass=ProxyMetaclass):

    def get_proxy(self, func):
        proxies = []
        for proxy in eval(('self.{}()'.format(func))):
            proxies.append(proxy)
        return proxies

    def crawl_xici(self):
        urls = ['http://www.xicidaili.com/nn/{}'.format(page) for page in range(1, 5)]
        for url in urls:
            print('正在抓取', url)
            response = get_page(url)
            ip_list = re.findall('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?(\d{2,6})', response, re.S)
            for li in ip_list:
                ip = li[0] + ':' + li[1]
                yield ip

    def crawl_kxdaili(self):
        urls = ['http://www.kxdaili.com/ipList/{}.html#ip'.format(page) for page in range(1, 6)]
        for url in urls:
            print('正在抓取', url)
            response = get_page(url)
            ip_list = re.findall('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?(\d{2,6})', response, re.S)
            for li in ip_list:
                ip = li[0] + ':' + li[1]
                yield ip

    def crawl_kuai(self):
        urls = ['https://www.kuaidaili.com/free/inha/{}'.format(page) for page in range(1, 5)]
        for url in urls:
            print('正在抓取', url)
            sleep(1)
            response = get_page(url)
            try:
                selector = etree.HTML(response)
                ip_list = selector.xpath('//tr/td[@data-title="IP"]/text()')
                ip_port = selector.xpath('//tr/td[@data-title="PORT"]/text()')
                for li, port in zip(ip_list, ip_port):
                    ip = li + ':' + port
                    yield ip
            except ValueError:
                pass

    def crawl_yun(self):
        urls = ['http://www.ip3366.net/free/?stype=1&page={}'.format(page) for page in range(1, 3)]
        for url in urls:
            print('正在抓取', url)
            header = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Cookie': 'UM_distinctid=1617063b823384-06e203960c10f5-3c604504-1fa400-1617063b824705; safedog-flow-item=; CNZZDATA1256284042=46895285-1518005811-null%7C1518230644',
                'Host': 'www.ip3366.net',
                'Referer': 'http://www.ip3366.net/free/?stype=1&page=6'
            }
            response = get_page(url, header)
            ip_list = re.findall('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?(\d{2,6})', response, re.S)
            for li in ip_list:
                ip = li[0] + ':' + li[1]
                yield ip


crawler = ProxyCrawler()

