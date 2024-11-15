# -*- coding:utf-8 -*-

from pydantic import BaseModel


class WeChatRequest(BaseModel):
    type: str
    offset: int
    count: int


class WeChatArticle(BaseModel):
    title: str
    author: str
    digest: str
    content: str
    content_source_url: str
    thumb_media_id: str
    show_cover_pic: int
    need_open_comment: int
    only_fans_can_comment: int
    url: str
    is_deleted: bool


class WeChatResponseItem(BaseModel):
    article_id: str
    content: list[WeChatArticle]
    update_time: int


class WeChatResponse(BaseModel):
    total_count: int
    item_count: int
    item: list[WeChatResponseItem]
