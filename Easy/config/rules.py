from collections import namedtuple

# 小说网站
BLACK_DOMAIN = ['www.qidian.com', 'www.zongheng.com']

# 搜索引擎
ENGINE_PRIORITY = ['baidu', '360', 'bing', ]

# 规则
Rules = namedtuple('Rules', 'content_url chapter_selector content_selector')
LatestRules = namedtuple('LatestRules', 'plan meta_value selector')

# 获取章节
PLAN_01 = LatestRules(
    True,
    {'latest_chapter_name': 'og:novel:latest_chapter_name', 'latest_chapter_url': 'og:novel:latest_chapter_url'},
    None,
)

LATEST_RULES = {
    "www.qidian.com": PLAN_01,
    "www.zongheng.com": PLAN_01
}