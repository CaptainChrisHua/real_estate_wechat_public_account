# -*- coding:utf-8 -*-
from fastapi import HTTPException

from src.api.wechat_views import wechat
from src.schemas.wechat_publish_schema import WeChatResponse
from src.services.wechat_publish_service import publisher


@wechat.post("/publish_list", response_model=WeChatResponse)
async def get_publish_list():
    try:
        result = publisher.get_publish_list()
        return result
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@wechat.post("/publish")
async def publish_article(media_id: str):
    try:
        result = await publisher.publish_article(media_id)
        return {"message": "Article published successfully", "data": result}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@wechat.post("/save_draft")
async def save_draft(draft_data: dict):
    try:
        result = await publisher.save_draft(draft_data)
        return {"message": "Draft saved successfully", "data": result}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
