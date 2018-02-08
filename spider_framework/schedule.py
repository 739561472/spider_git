# encoding: utf-8
import asyncio
import pickle
import os
from redis_db import RedisQueue
from downloader import Spider
from config import MAX


class Scheduler(object):
    def __init__(self):
        self.save_q = RedisQueue('save')
        self.work_q = RedisQueue('work')

    def format_data(self, args, callback):
        self.callback = callback
        if not isinstance(args, dict):
            print('args参数必须以字典形式传入')
            os._exit(0)
        elif 'url' not in args.keys():
            print('缺少url')
            os._exit(0)
        self.work_q.put(pickle.dumps(args))

    async def work_task(self, task_args):
        self.spider = Spider(task_args)
        response = await self.spider.fetch()
        if self.callback:
            self.save_q.put(self.callback(response))
        else:
            return None

    def start_task(self):
        count = self.work_q.count()
        while count:
            if count < MAX:
                task = [self.work_task(task_args=self.work_q.get_nowait()) for _ in range(count)]
            else:
                task = [self.work_task(task_args=self.work_q.get_nowait()) for _ in range(MAX)]
            loop = asyncio.get_event_loop()
            try:
                loop.run_until_complete(asyncio.gather(*task))
            except RuntimeError:
                return None
            loop.close()


def parse(response):
    print(response)



