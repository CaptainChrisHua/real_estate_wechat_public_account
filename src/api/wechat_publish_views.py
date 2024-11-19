# -*- coding:utf-8 -*-
from fastapi import UploadFile

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


@wechat.post("/save_draft")
async def save_draft(draft_data: dict):
    result = await publisher.save_draft(draft_data)
    return {"message": "Draft saved successfully", "data": result}


@wechat.post("/add_material")
async def add_material(file: UploadFile):
    result = await publisher.add_material(file)
    return {"message": "Material added successfully", "data": result}
