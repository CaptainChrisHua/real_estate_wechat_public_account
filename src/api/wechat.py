# -*- coding:utf-8 -*-
from fastapi import Request, HTTPException, APIRouter
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.utils import check_signature

from src.conf.config import PUB_APP_TOKEN

wechat = APIRouter(prefix="/api/v1/wechat", tags=["wechat"])


@wechat.get("/")
async def wechat_verify(signature: str, timestamp: str, nonce: str, echostr: str):
    try:
        # 使用 wechatpy 的 check_signature 函数来验证请求是否合法
        check_signature(PUB_APP_TOKEN, signature, timestamp, nonce)
        return echostr  # 验证通过，返回 echostr 作为响应
    except InvalidSignatureException:
        raise HTTPException(status_code=403, detail="Invalid signature")


@wechat.post("/")
async def wechat_message(request: Request):
    # 处理微信的消息请求
    xml = await request.body()
    # 这里你可以解析 xml，并根据业务逻辑处理消息
    print(xml)
    return "success"
