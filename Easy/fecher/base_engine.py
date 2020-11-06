import aiohttp
import async_timeout

from Easy.config import CONFIG, LOGGER, BLACK_DOMAIN, LATEST_RULES


class BaseNovels:
    """
    小说抓取父类
    """

    def __init__(self, logger=None):
        self.black_domain = BLACK_DOMAIN
        self.config = CONFIG
        self.latest_rules = LATEST_RULES
        self.logger = logger if logger else LOGGER

    # 公共抓取函数
    async def fetch_url(self, url, params, headers):
        with async_timeout.timeout(15):
            try:
                async with aiohttp.ClientSession() as client:
                    async with client.get(url, params=params, headers=headers) as response:
                        assert response.status == 200
                        LOGGER.info('Task url: {}'.format(response.url))
                        try:
                            text = await response.text()
                        except:
                            text = await response.read()
                        return text
            except Exception as e:
                LOGGER.exception(e)
                return None

    @classmethod
    async def start(cls, novels_name):
        return await cls().novels_search(novels_name)

    # 小说抓取函数
    async def data_extraction(self, html):
        raise NotImplementedError

    # 小说搜索
    async def novels_search(self, novels_name):
        raise NotImplementedError