# -*- coding:utf-8 -*-
from fastapi import UploadFile, APIRouter

from src.schemas.wechat_publish_schema import WeChatRequest
from src.services.wechat_materials import wechat_materials

materials = APIRouter(prefix="/api/v1/materials", tags=["materials"])


@materials.get("/get_material_list")
async def get_material_list(material_type: str = "image", offset: int = 0, count: int = 20):
    result = await wechat_materials.get_material_list(material_type, offset, count)
    return {"message": "Get material list successfully", "data": result}


@materials.post("/add_material")
async def add_material(file: UploadFile):
    result = await wechat_materials.add_material(file)
    return {"message": "Material added successfully", "data": result}