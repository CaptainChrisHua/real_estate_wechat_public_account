# -*- coding:utf-8 -*-
from typing import List

from fastapi import APIRouter, UploadFile, File, Request
from src.api import SuccessResponse

api_v1 = APIRouter(prefix="/api/v1")


# @api_v1.post('/hello_world', tags=["XXX接口 API V1.0"], summary="示例接口", response_model=PeerResponseSchema)
# async def peer_service(params: PeerSchema):
#     data = hello_world(params)
#     return SuccessResponse(data=data, msg="获取成功")


# @api_v1.post("/file/")
# async def file_(file: List[bytes] = File(...)):
#     # 存储内存中，适合小文件
#     return {"file_size": len(file)}


@api_v1.post("/uploadfile/", tags=["UTC接口 API V1.0"], summary="文件上传")
async def upload_files(files: List[UploadFile] = File(...)):
    # 内存不够用时，文件存储到磁盘中，适合上传大文件
    result = []
    for file in files:
        with open(file.filename, "wb") as f:
            f.write(await file.read())
        result.append({
            "filename": file.filename,
            "content-type": file.content_type,
        })
    return result

