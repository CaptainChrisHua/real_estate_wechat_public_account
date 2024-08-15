# -*- coding:utf-8 -*-

from src.services.wechat_service import fetch_access_token
from src.utils import logger


async def refresh_access_token():
    try:
        await fetch_access_token()
        logger.info("Access token refreshed successfully.")
    except Exception as e:
        logger.info(f"Failed to refresh access token: {e}")


def task2():
    pass
