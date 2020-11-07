import asyncio

from aiocache.serializers import PickleSerializer
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from Easy.fecher.decorator import cached
from Easy.fecher.fetcher_function import get_random_user_agent
from Easy.fecher.base_engine import BaseNovels


class BingNovels(BaseNovels):

    def __init__(self):
        super(BingNovels, self).__init__()

    # 小说抓取
    async def data_extraction(self, html):
        try:
            title = html.select('h2 a')[0].get_text()
            url = html.select('h2 a')[0].get('href', None)
            netloc = urlparse(url).netloc
            url = url.replace('index.html', '').replace('Index.html', '')
            if not url or 'baidu' in url or 'baike.so.com' in url or netloc in self.black_domain or '.html' in url:
                return None
            is_parse = 1 if netloc in self.rules.keys() else 0
            is_recommend = 1 if netloc in self.latest_rules.keys() else 0
            timestamp = 0
            time = ''
            return {'title': title,
                    'url': url,
                    'time': time,
                    'is_parse': is_parse,
                    'is_recommend': is_recommend,
                    'timestamp': timestamp,
                    'netloc': netloc}

        except Exception as e:
            self.logger.exception(e)
            return None

    # 获取必应url
    async def novels_search(self, novels_name):
        url = self.config.BY_URL
        headers = {
            'user-agent': await get_random_user_agent(),
            'referer': "https://www.bing.com/"
        }
        params = {'q': novels_name, 'ensearch': 0}
        html = await self.fetch_url(url=url, params=params, headers=headers)
        if html:
            soup = BeautifulSoup(html, 'html5lib')
            result = soup.find_all(class_='b_algo')
            extra_tasks = [self.data_extraction(html=i) for i in result]
            tasks = [asyncio.ensure_future(i) for i in extra_tasks]
            done_list, pending_list = await asyncio.wait(tasks)
            res = [task.result() for task in done_list if task.result()]
            return res
        else:
            return []


@cached(ttl=259200, key_from_attr='novels_name', serializer=PickleSerializer(), namespace="novels_name")
async def start(novels_name):
    """
    Start spider
    :return:
    """
    return await BingNovels.start(novels_name)