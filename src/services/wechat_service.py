# -*- coding:utf-8 -*-

import json
import os
from datetime import datetime, timedelta

import httpx

from config.config import PUB_APP_ID, PUB_APP_SECRET
from src.utils import logger

TOKEN_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                               "wechat_access_token.json")


async def fetch_access_token() -> str:
    url = (f"https://api.weixin.qq.com/cgi-bin/token?grant_type="
           f"client_credential&appid={PUB_APP_ID}&secret={PUB_APP_SECRET}")
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            if "access_token" in data:
                expires_in = data["expires_in"]
                logger.info(f"access_token: {data['access_token']}")
                save_access_token(data["access_token"], expires_in)
                return data["access_token"]
            else:
                raise Exception(f"Error fetching access token: {data}")
        else:
            raise Exception(f"HTTP error: {response.status_code}")


# def save_access_token(token: str, expires_in: int):
#     # 保存access_token到Redis并设置过期时间
#     redis_util.setex("wechat_access_token", timedelta(seconds=expires_in), value=token)
#     logger.info(f"Saving access token: {token}")
#
#
# def load_access_token() -> str:
#     token = redis_util.get("wechat_access_token")
#     if token:
#         return token
#     else:
#         raise Exception("Access token not found or expired")


def save_access_token(token: str, expires_in: int):
    # 计算过期时间
    expires_at = datetime.now() + timedelta(seconds=expires_in)
    # 构造保存的数据
    data = {
        "token": token,
        "expires_at": expires_at.strftime("%Y-%m-%d %H:%M:%S")
    }
    # 将数据保存到本地文件
    with open(TOKEN_FILE_PATH, "w") as file:
        json.dump(data, file)
    logger.info(f"Access token saved to file with expiration at {expires_at}")


def load_access_token() -> str:
    # 检查文件是否存在
    if not os.path.exists(TOKEN_FILE_PATH):
        raise Exception("Access token file not found")

    with open(TOKEN_FILE_PATH, "r") as file:
        data = json.load(file)

    # 检查过期时间
    expires_at = datetime.strptime(data["expires_at"], "%Y-%m-%d %H:%M:%S")
    if datetime.now() < expires_at:
        return data["token"]
    else:
        raise Exception("Access token expired")
