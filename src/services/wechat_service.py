# -*- coding:utf-8 -*-
from datetime import timedelta

import httpx

from src.conf.config import PUB_APP_ID, PUB_APP_SECRET
from src.utils import redis_util, logger


async def fetch_access_token() -> str:
    url = (f"https://api.weixin.qq.com/cgi-bin/token?grant_type="
           f"client_credential&appid={PUB_APP_ID}&secret={PUB_APP_SECRET}")
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            if "access_token" in data:
                expires_in = data["expires_in"]
                save_access_token(data["access_token"], expires_in)
                logger.info(f"access_token: {data['access_token']}")
                return data["access_token"]
            else:
                raise Exception(f"Error fetching access token: {data}")
        else:
            raise Exception(f"HTTP error: {response.status_code}")


def save_access_token(token: str, expires_in: int):
    # 保存access_token到Redis并设置过期时间
    redis_util.setex("wechat_access_token", timedelta(seconds=expires_in), value=token)
    logger.info(f"Saving access token: {token}")


def load_access_token() -> str:
    token = redis_util.get("wechat_access_token")
    if token:
        return token
    else:
        raise Exception("Access token not found or expired")
