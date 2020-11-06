import asyncio
import os
import schedule
import sys
import time

os.environ['MODE'] = 'PRO'
sys.path.append('../../')

from Easy.fecher.cache import update_all_books

loop = asyncio.get_event_loop()


def update_all_books_schedule():
    task = asyncio.ensure_future(update_all_books(loop))
    loop.run_until_complete(task)
    return task.result() or None


# python novels_schedule.py
schedule.every(180).minutes.do(update_all_books_schedule)

while True:
    schedule.run_pending()
    time.sleep(1)