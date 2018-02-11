import pymongo
import time
import aiohttp
import asyncio
from lxml import etree


client = pymongo.MongoClient(host='127.0.0.1', port='27017')
db = client['czone']
queue = asyncio.Queue()


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def send(url):
    async with aiohttp.ClientSession() as session:
        response = await fetch(session, url)
        parse(response)


def parse(response):
    selector = etree.HTML(response)
    for item in selector.xpath('//tr[@class="table-plate3"]'):
        company_title = item.xpath('.//span[@class="tp2_tit"]/a/text()')[0]
        company = item.xpath('.//span[@class="tp2_com"]/text()')[0]
        money = item.xpath('.//div[@class="money"]/text()')[0]
        time = item.xpath('./td/text()')[8]
        investor = item.xpath('.//td[@class="tp3"]/@title')[0]
        industry = [_ for _ in item.xpath('./td/a/text()')]
        date = item.xpath('.//td[last()-1]/text()')[-1]
        data = {
            'company_title': company_title,
            'company': company,
            'money': money,
            'time': time,
            'investor': investor,
            'industry': industry,
            'date': date
        }
        queue.put(data)


def pipelines(data):
    if '详情' in data.get('industry'):
        data.get('industry').remove('详情')
    save_to_mongo(data)


def save_to_mongo(item):
    if db['invest'].insert(item):
        print('插入成功！', item)


def scheduler():
    loop = asyncio.get_event_loop()
    for i in range(1, 1090, 5):
        task = [send('http://www.cyzone.cn/event/list-764-0-{page}-0-0-0-0/'.format(page=i+page)) for page in range(5)]
        loop.run_until_complete(asyncio.wait(task))
        time.sleep(1)
    loop.close()
    while not queue.empty():
        data = queue.get()
        pipelines(data)


if __name__ == '__main__':
    scheduler()


