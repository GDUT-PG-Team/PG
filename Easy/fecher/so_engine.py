import asyncio

from aiocache.serializers import PickleSerializer
from bs4 import BeautifulSoup
from urllib.parse import parse_qs, urlparse

from Easy.fecher.fetcher_function import get_random_user_agent
from Easy.fecher.base_engine import BaseNovels


class SoNovels(BaseNovels):

    def __init__(self):
        super(SoNovels, self).__init__()

    # 小说抓取
    async def data_extraction(self, html):
        try:
            # 2017.09.09 修改 更加全面地获取title && url
            try:
                title = html.select('h3 a')[0].get_text()
                url = html.select('h3 a')[0].get('href', None)
            except Exception as e:
                self.logger.exception(e)
                return None

            # 针对不同的请进行url的提取
            if "www.so.com/link?m=" in url:
                url = html.select('h3 a')[0].get('data-mdurl', None)
            if "www.so.com/link?url=" in url:
                url = parse_qs(urlparse(url).query).get('url', None)
                url = url[0] if url else None

            netloc = urlparse(url).netloc
            if not url or 'baidu' in url or 'baike.so.com' in url or netloc in self.black_domain:
                return None
            is_parse = 1 if netloc in self.rules.keys() else 0
            is_recommend = 1 if netloc in self.latest_rules.keys() else 0
            time = ''
            timestamp = 0
            return {'title': title, 'url': url.replace('index.html', '').replace('Index.html', ''), 'time': time,
                    'is_parse': is_parse,
                    'is_recommend': is_recommend,
                    'timestamp': timestamp,
                    'netloc': netloc}
        except Exception as e:
            self.logger.exception(e)
            return None

    # 获取必应url
    async def novels_search(self, novels_name):
        url = self.config.SO_URL

        headers = {
            'User-Agent': await get_random_user_agent(),
            'Referer': "http://www.so.com/haosou.html?src=home"
        }
        params = {'ie': 'utf-8', 'src': 'noscript_home', 'shb': 1, 'q': novels_name, }
        html = await self.fetch_url(url=url, params=params, headers=headers)
        if html:
            soup = BeautifulSoup(html, 'html5lib')
            result = soup.find_all(class_='res-list')
            extra_tasks = [self.data_extraction(html=i) for i in result]
            tasks = [asyncio.ensure_future(i) for i in extra_tasks]
            done_list, pending_list = await asyncio.wait(tasks)
            res = [task.result() for task in done_list if task.result()]
            return res
        else:
            return []

