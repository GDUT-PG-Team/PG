# 配置文件夹

import os
import logging

from .rules import *

logging_format = "[%(asctime)s] %(process)d-%(levelname)s "
logging_format += "%(module)s::%(funcName)s():l%(lineno)d: "
logging_format += "%(message)s"

logging.basicConfig(
    format=logging_format,
    level=logging.DEBUG
)
LOGGER = logging.getLogger()


# 加载配置
def load_config():
    os.environ['MODE'] = 'PRO'
    mode = os.environ.get('MODE', 'DEV')
    LOGGER.info('Easy 启动模式：{}'.format(mode))
    try:
        if mode == 'PRO':
            from .pro_config import ProConfig
            return ProConfig
        elif mode == 'DEV':
            from .dev_config import DevConfig
            return DevConfig
        else:
            from .dev_config import DevConfig
            return DevConfig
    except ImportError:
        from .config import Config
        return Config


CONFIG = load_config()