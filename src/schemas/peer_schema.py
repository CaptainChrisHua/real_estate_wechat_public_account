# -*- coding:utf-8 -*-
from typing import List, Optional

from pydantic import Field, BaseModel

from src.schema import BaseRespSchema


class PeerSchema(BaseModel):
    """
    同行推荐Schema
    """
    name: str = Field(None, alias='company_name', description='企业名称')
    econ_kind_code_list: Optional[List[str]] = Field(None, description='企业类型代码')
    size: Optional[int] = Field(30, description='同行数量')

    debug: int = Field(0, repr=False)
    set_area_weight: int = Field(1, repr=False)
    set_cgoe_weight: int = Field(1, repr=False)

    class Config:

        @staticmethod
        def schema_extra(schema):
            exclude = [
                'debug', 'set_area_weight', 'set_cgoe_weight'
            ]
            for i in exclude:  # 从swagger文档中删除不需要的字段
                schema['properties'].pop(i, None)


class Reason(BaseModel):
    content: Optional[str] = Field(None, description='推荐关键词')
    type: Optional[int] = Field(None, description='理由来源 0:用户手标 1：同行推荐 2：国三推荐')


class Datum(BaseModel):
    _id: Optional[str] = Field(None, description='es的_id')
    reason: Optional[Reason] = Field(None, description=' ')
    reason_for_display: Optional[str] = Field(
        None,
        description="展示的推荐理由",
    )


class PeerResponseSchema(BaseRespSchema):
    data: List[Datum] = Field([], description='返回数据')  # 嵌套类型
