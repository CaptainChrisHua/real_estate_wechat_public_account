# -*- coding:utf-8 -*-
from typing import List

from pydantic import Field
from pydantic.main import BaseModel


class BaseRespSchema(BaseModel):
    code: int = Field(200, description='code')
    data: List = Field([], description='返回数据')
    msg: str = Field("", description='响应信息')
    success: bool = Field(True, description='请求成功为True，失败为False')
