# -*- coding:utf-8 -*-
import hashlib

from fastapi import APIRouter, HTTPException, Request, Response

from src.conf.config import PUB_APP_TOKEN
from src.utils import logger

wechat = APIRouter(prefix="/api/v1/wechat", tags=["wechat"])


def check_signature(signature: str, timestamp: str, nonce: str) -> bool:
    # 将token、timestamp、nonce三个参数进行字典序排序
    tmp_arr = [PUB_APP_TOKEN, timestamp, nonce]
    tmp_arr.sort()

    # 将三个参数字符串拼接成一个字符串
    tmp_str = ''.join(tmp_arr)

    # 对拼接后的字符串进行sha1加密
    tmp_str = hashlib.sha1(tmp_str.encode('utf-8')).hexdigest()
    return tmp_str == signature


@wechat.get('/')
async def wechat_verify(signature: str, timestamp: str, nonce: str, echostr: str):
    # 校验signature
    if check_signature(signature, timestamp, nonce):
        # 校验通过，返回echostr
        return Response(content=echostr, media_type="text/plain;charset=UTF-8")
    else:
        # 校验失败，抛出HTTP异常
        raise HTTPException(status_code=403, detail="Verification failed")


@wechat.post("/")
async def wechat_message(request: Request):
    # 处理微信的消息请求
    xml = await request.body()
    # 这里你可以解析 xml，并根据业务逻辑处理消息
    logger.info(xml)
    return "success"
