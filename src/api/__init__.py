# -*- coding:utf-8 -*-
import traceback

from elasticsearch.exceptions import RequestError, BadRequestError
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from fastapi import HTTPException, status

from src.utils import logger


class CodeMsg(object):
    """
    api响应结果编码与信息
    """

    def __init__(self, code: int, msg: str):
        self.code = code
        self.msg = msg


class ResponseEnum(object):
    """
    api响应结果
    """
    PARAMS_EXCEPTION = CodeMsg(4001, "Parameter Error")

    NOT_FOUND = CodeMsg(4004, "URL Not Found")
    BAD_REQUEST = CodeMsg(4002, "Bad Request")

    INTERNAL_ERROR = CodeMsg(5001, "Internal Server Error")


class BaseResponse(JSONResponse):

    def __init__(self, code, data, msg, success, **kwargs):
        result = dict(code=code, data=data, msg=msg, success=success, **kwargs)
        JSONResponse.__init__(self, content=result)


class SuccessResponse(JSONResponse):

    def __init__(self, data, msg, **kwargs):
        result = dict(code=200, data=data, msg=msg, success=True, **kwargs)
        JSONResponse.__init__(self, content=result)


class FailResponse(JSONResponse):

    def __init__(self, code, msg, **kwargs):
        result = dict(code=code, data={}, msg=msg, success=False, **kwargs)
        JSONResponse.__init__(self, content=result)


def error_handler(error):
    tb = traceback.format_exc()
    error_content = tb.split("File")[-1].replace("\n", ",")
    # 请求参数异常
    if isinstance(error, ValidationError):
        logger.warning(error_content)
        return FailResponse(code=ResponseEnum.BAD_REQUEST.code, msg=ResponseEnum.BAD_REQUEST.msg)

    # 返回数据格式异常
    if isinstance(error, ResponseValidationError):
        logger.warning(error_content)
        return FailResponse(code=ResponseEnum.BAD_REQUEST.code, msg=ResponseEnum.BAD_REQUEST.msg)

    # ES连接异常
    if isinstance(error, RequestError):
        logger.warning(error_content)
        return FailResponse(code=error.status_code, msg=error.error)

    # badrequest
    if isinstance(error, BadRequestError):
        logger.warning(error_content)
        return FailResponse(code=ResponseEnum.BAD_REQUEST.code, msg=ResponseEnum.BAD_REQUEST.msg)

    # not found
    if isinstance(error, BadRequestError):
        logger.warning(error_content)
        return FailResponse(code=ResponseEnum.NOT_FOUND.code, msg=ResponseEnum.NOT_FOUND.msg)

    # HTTP 错误
    if isinstance(error, HTTPException):
        logger.warning(error_content)
        return FailResponse(code=ResponseEnum.NOT_FOUND.code, msg=ResponseEnum.NOT_FOUND.msg)

    else:
        logger.error(error_content)
        # 最后在error_log中打印完整的错误日志
        logger.error(tb)
        return FailResponse(code=ResponseEnum.INTERNAL_ERROR.code, msg=ResponseEnum.INTERNAL_ERROR.msg)
