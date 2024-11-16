# -*- coding:utf-8 -*-
import traceback

from src.services.wechat_service import fetch_access_token
from src.utils import logger


async def refresh_access_token():
    try:
        await fetch_access_token()
        logger.info("Access token refreshed successfully.")
    except Exception as e:
        logger.error(f"Failed to refresh access token: {e}")
        logger.error(traceback.format_exc())


def task2():
    pass
