# -*- coding:utf-8 -*-
import httpx
from fastapi import FastAPI, HTTPException

from src.schemas.wechat_publish_schema import WeChatRequest
from src.utils import logger
from src.utils.wechat_access_token import get_access_token

app = FastAPI()


class WeChatPublisher:
    def __init__(self):
        self.base_url = "https://api.weixin.qq.com/cgi-bin"

    async def get_publish_list(self, we_request: WeChatRequest):
        url = f"https://api.weixin.qq.com/cgi-bin/freepublish/batchget?access_token={get_access_token()}"
        logger.info(f"url: {url}")
        data = we_request.dict()
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch data from WeChat API")

        response_data = response.json()
        logger.info(f"Response data: {response_data}")
        # You can process the response_data here if needed
        return response_data

    async def save_draft(self, draft_data: dict) -> dict:
        url = f"{self.base_url}/draft/add?access_token={get_access_token()}"
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=draft_data)
            if response.status_code == 200:
                result = response.json()
                if result.get("errcode") == 0:
                    return result
                else:
                    raise HTTPException(status_code=400, detail=result)
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)

    async def publish_article(self, media_id: str) -> dict:
        url = f"{self.base_url}/freepublish/submit?access_token={get_access_token()}"
        data = {"media_id": media_id}
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data)
            if response.status_code == 200:
                result = response.json()
                if result.get("errcode") == 0:
                    return result
                else:
                    raise HTTPException(status_code=400, detail=result)
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)


publisher = WeChatPublisher()
