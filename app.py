# -*- coding:utf-8 -*-

import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

from src.api import error_handler
from src.api.views import api_v1
from src.api.wechat_views import wechat
from src.crontab import scheduler, refresh_access_token


# from src.conf.config import REDIS_ALGORITHMS
# from src.crontab import scheduler
#
# from uvicorn.config import LOGGING_CONFIG

# LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
# LOGGING_CONFIG = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "formatters": {
#         "default": {
#             "()": "uvicorn.logging.DefaultFormatter",
#             "fmt": "%(levelprefix)s %(message)s",
#             "use_colors": None,
#         },
#         "access": {
#             "()": "uvicorn.logging.AccessFormatter",
#             "fmt": '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',
#         },
#     },
#     "handlers": {
#         "default": {
#             "formatter": "default",
#             "class": "logging.handlers.TimedRotatingFileHandler",
#             "filename": "./log"
#         },
#         "access": {
#             "formatter": "access",
#             "class": "logging.handlers.TimedRotatingFileHandler",
#             "filename": "./log"
#
#         },
#     },
#     "loggers": {
#         "": {"handlers": ["default"], "level": "INFO"},
#         "uvicorn.error": {"level": "INFO"},
#         "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
#     }
# }

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时手动触发一次token刷新，确保Redis中有有效的token
    await refresh_access_token()
    # 添加定时任务，每两小时刷新一次token
    scheduler.start()  # 启动调度器
    yield
    scheduler.shutdown()  # 关闭调度器


app = FastAPI(lifespan=lifespan, docs_url="/apidocs")

app.mount(path='/static', app=StaticFiles(directory="static"), name="static")

# # 将发起请求都接入链路追踪
# install_patches(patchers=[
#     "opentracing_instrumentation.client_hooks.requests.install_patches",
#     "opentracing_instrumentation.client_hooks.urllib.install_patches",
#     "opentracing_instrumentation.client_hooks.urllib2.install_patches",
# ])

# # 接入链路追踪
# @app.on_event('startup')
# async def startup():
#     settings.jaeger_host = '127.0.0.1'
#     settings.jaeger_port = 6831
#     settings.service_name = os.environ.get("APP_NAME", "wzalgo-fastapi-template")
#     settings.trace_id_header = "TraceID"
#     settings.jaeger_sampler_type = "probabilistic"
#     settings.jaeger_sampler_rate = 0.1
#     setup_opentracing(app)
#     app.add_middleware(FastApiOpentracingMiddleware)
#     LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"


# 注册蓝图，即多个模块
app.include_router(api_v1)
app.include_router(wechat)


@app.get('/test')
def test():
    return 'ok'


# # 加锁，只有首次启动的worker执行定时任务，防止多worker启动多次定时任务
# redis_util = RedisUtil(REDIS_ALGORITHMS)
# try:
#     lock = redis_util.setnx(f"{REDIS_ALGORITHMS}:apscheduler_lock", "expire_in_300_seconds")
#     redis_util.expire(f"{REDIS_ALGORITHMS}:apscheduler_lock", 300)
# except Exception:
#     redis_util.delete(f"{REDIS_ALGORITHMS}:apscheduler_lock")
#     lock = False
# if lock:
#   scheduler.start()  # 开启定时任务


# @app.middleware("http")
# async def before_request(request: Request, call_next):
#     if request.method == "POST":
#         params = request.json()
#         api = request.url.path
#         if request.headers.getlist("X-Forwarded-For"):
#             ip = request.headers.getlist("X-Forwarded-For")[0]
#         else:
#             ip = request.client.host
#         logger.info(f"调用接口{api}，入参为{params}，IP为{ip}")
#     response = await call_next(request)
#     return response


# 统一异常处理
@app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, exc: Exception):
    response = error_handler(exc)
    return response


@app.get("/upload", tags=["UTC接口 API V1.0"], summary="文件上传页面")
async def upload_page():
    return FileResponse('static/upload.html')


if __name__ == '__main__':
    env_port = os.environ.get('APP_PORT', 4568)
    uvicorn.run("app:app", host='0.0.0.0', port=int(env_port))
