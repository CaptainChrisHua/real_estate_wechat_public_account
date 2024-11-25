# -*- coding:utf-8 -*-

from src.api.wechat_views import wechat
from src.schemas.wechat_publish_schema import WeChatRequest
from src.services.wechat_publish_service import publisher


@wechat.post("/publish_list")
async def get_publish_list(we_request: WeChatRequest):
    result = await publisher.get_publish_list(we_request)
    return result


@wechat.post("/publish")
async def publish_article(media_id: str):
    result = await publisher.publish_article(media_id)
    return {"message": "Article published successfully", "data": result}


@wechat.post("/get_status")
async def get_publish_status(publish_id: str):
    result = await publisher.get_publish_status(publish_id)
    return {"message": "Get publish status successfully", "data": result}


@wechat.post("/send_mass_message")
async def send_mass_message(is_to_all: bool, tag_id: int = None, media_id: str = None):
    result = await publisher.send_mass_message(is_to_all, tag_id, media_id)
    return {"message": "Sent mass message successfully", "data": result}


@wechat.post("/save_draft")
async def save_draft(draft_data: dict):
    result = await publisher.save_draft(draft_data)
    return {"message": "Draft saved successfully", "data": result}


@wechat.get("/get_draft_list")
async def get_draft_list(offset: int, count: int, no_content: int = 1):
    result = await publisher.get_draft_list(offset, count, no_content)
    return {"message": "Get draft list successfully", "data": result}
