# -*- coding:utf-8 -*-
import json

import httpx
from fastapi import FastAPI, HTTPException

from src.utils.wechat_access_token import get_access_token

app = FastAPI()


class WeChatPublisher:
    def __init__(self):
        self.base_url = "https://api.weixin.qq.com/cgi-bin"

    async def save_draft(self, draft_data):
        url = f"{self.base_url}/draft/add?access_token={get_access_token()}"
        draft_data = json.dumps(draft_data, ensure_ascii=False)
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=draft_data)
            if response.status_code == 200:
                result = response.json()
                if result.get("errcode") == 0:
                    return result
                else:
                    raise HTTPException(status_code=400, detail=result)
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)

    async def get_draft_list(self, offset: int, count: int, no_content: int = 1) -> dict:
        """
        获取草稿列表的方法
        :param offset: 从素材的该偏移位置开始返回，0表示从第一个素材返回
        :param count: 返回素材的数量，取值在1到20之间
        :param no_content: 1表示不返回content字段，0表示正常返回（默认为0）
        :return: 返回草稿列表的字典
        """
        if not (1 <= count <= 20):
            raise ValueError("count must be between 1 and 20.")

        url = f"{self.base_url}/draft/batchget?access_token={get_access_token()}"
        payload = {
            "offset": offset,
            "count": count,
            "no_content": no_content
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            if response.status_code == 200:
                result = response.json()
                if "errcode" not in result or result["errcode"] == 0:
                    return result
                else:
                    raise HTTPException(status_code=400, detail=result)
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)

    async def send_mass_message(self, is_to_all: bool, tag_id: int = None, media_id: str = None) -> dict:
        """
        Sends a mass message to users based on tag or to all users.
        :param is_to_all: Boolean indicating whether to send to all users.
        :param tag_id: Tag ID for targeted users (ignored if is_to_all is True).
        :param media_id: Media ID of the content to send.
        :return: Response from the WeChat API.
        """
        url = f"{self.base_url}/message/mass/sendall?access_token={get_access_token()}"

        # Constructing the request payload
        data = {
            "filter": {
                "is_to_all": is_to_all
            },
            "mpnews": {
                "media_id": media_id
            },
            "msgtype": "mpnews",
            "send_ignore_reprint": 0
        }

        # Add tag_id if targeting a specific group
        if not is_to_all:
            if tag_id is None:
                raise ValueError("tag_id must be provided when is_to_all is False.")
            data["filter"]["tag_id"] = tag_id

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data)
            if response.status_code == 200:
                result = response.json()
                if result.get("errcode") == 0:
                    return result  # Success
                else:
                    raise HTTPException(status_code=400, detail=result)
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)


publisher = WeChatPublisher()
