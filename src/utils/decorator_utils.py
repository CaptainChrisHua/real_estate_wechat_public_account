# -*- coding:utf-8 -*-

import functools
import time

from src.utils import logger


def timer(func):
    """计时器"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        time_used = round(time.time() - start, 3)
        if time_used < 1:
            logger.info(f'执行函数{func.__name__}，耗时{time_used}秒')
        else:
            logger.warning(f'执行函数{func.__name__}，耗时{time_used}秒')
        return res

    return wrapper
