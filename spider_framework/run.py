from time import time

import requests

from schedule import Scheduler, parse


def run(url, headers=None, ip=None, timeout=None, callback=parse):
    scheduler = Scheduler()
    start = time()
    for _ in range(100):
        scheduler.format_data(args={
            "url": url,
            "headers": headers,
            "ip": ip,
            "timeout": timeout
        }, callback=callback)

    scheduler.start_task()
    #     res = requests.get(url)
    print(time()-start)


if __name__ == '__main__':
    url = 'http://www.baidu.com'
    run(url)
