# -*- coding:utf-8 -*-
from src.utils.es_util import EsApiUtil
from src.utils.redis_util import RedisUtil
from src.utils.log_utils import LogUtil

from src.conf.config import LOG_PATH, LOG_LEVEL

logger = LogUtil(log_path=LOG_PATH, log_level=LOG_LEVEL)
# redis_util = RedisUtil(REDIS_ALGORITHMS)
# es_api_util = EsApiUtil(ENV,
#                         "wzalgo-fastapi-template",
#                         "enterprise",
#                         REDIS_ALGORITHMS)
