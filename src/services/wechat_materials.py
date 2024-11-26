# -*- coding:utf-8 -*-
import httpx
from fastapi import HTTPException, UploadFile

from src.utils.wechat_access_token import get_access_token


class WeChatMaterials:

    def __init__(self):
        self.base_url = "https://api.weixin.qq.com/cgi-bin"

    async def add_material(self, file: UploadFile) -> dict:
        """
        Uploads an image to WeChat to get a media_id.
        """
        url = f"{self.base_url}/material/add_material?access_token={get_access_token()}&type=image"
        headers = {"Content-Type": "multipart/form-data"}

        # Preparing the file for upload
        files = {"media": (file.filename, file.file, file.content_type)}

        async with httpx.AsyncClient() as client:
            response = await client.post(url, files=files, headers=headers)
            if response.status_code == 200:
                result = response.json()
                return result
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)

    async def get_material_list(self, material_type: str, offset: int = 0, count: int = 20) -> dict:
        """
        Fetches the list of permanent materials from WeChat.
        """
        # Validate input
        if material_type not in ["image", "video", "voice", "news"]:
            raise ValueError("Invalid material type. Must be one of ['image', 'video', 'voice', 'news'].")
        if not (1 <= count <= 20):
            raise ValueError("Count must be between 1 and 20.")

        url = f"{self.base_url}/material/batchget_material?access_token={get_access_token()}"
        payload = {
            "type": material_type,
            "offset": offset,
            "count": count
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            if response.status_code == 200:
                result = response.json()
                if "errcode" not in result:
                    return result
                else:
                    raise HTTPException(status_code=400, detail=result)
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)


async def image_proxy(url: str):
    headers = {
        'Referer': 'https://mp.weixin.qq.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)


wechat_materials = WeChatMaterials()
