# # -*- coding:utf-8 -*-
# import asyncio
# import logging
# from datetime import datetime
#
# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.triggers.date import DateTrigger
# from fastapi import FastAPI, HTTPException
#
# # 初始化 FastAPI 应用
# app = FastAPI()
#
# # 初始化 APScheduler
# scheduler = BackgroundScheduler()
# scheduler.start()
#
#
# # 模拟发布任务逻辑
# async def send_mass_message_task(is_to_all: bool, tag_id: int, media_id: str):
#     logging.info(f"Sending mass message: is_to_all={is_to_all}, tag_id={tag_id}, media_id={media_id}")
#     # 模拟推送处理
#     await asyncio.sleep(1)  # 模拟任务延迟
#     logging.info("Mass message sent successfully!")
#
#
# # 定时任务接口
# @app.post("/schedule_mass_message")
# async def schedule_mass_message(
#         schedule_time: datetime,
#         is_to_all: bool,
#         tag_id: int = None,
#         media_id: str = None
# ):
#     if schedule_time <= datetime.now():
#         raise HTTPException(status_code=400, detail="Schedule time must be in the future.")
#
#     # 创建定时任务
#     trigger = DateTrigger(run_date=schedule_time)
#     scheduler.add_job(
#         send_mass_message_task,
#         trigger=trigger,
#         kwargs={"is_to_all": is_to_all, "tag_id": tag_id, "media_id": media_id},
#         id=f"mass_message_{schedule_time.timestamp()}",  # 任务ID
#         replace_existing=True  # 如果有重复ID则替换
#     )
#     return {"message": "Scheduled mass message successfully!", "schedule_time": schedule_time}
#
#
# # 获取当前任务列表
# @app.get("/scheduled_jobs")
# def get_scheduled_jobs():
#     jobs = scheduler.get_jobs()
#     job_list = [
#         {
#             "id": job.id,
#             "next_run_time": job.next_run_time,
#             "trigger": str(job.trigger),
#         }
#         for job in jobs
#     ]
#     return {"jobs": job_list}
#
#
# # 删除定时任务
# @app.delete("/cancel_job/{job_id}")
# def cancel_job(job_id: str):
#     job = scheduler.get_job(job_id)
#     if not job:
#         raise HTTPException(status_code=404, detail="Job not found")
#     job.remove()
#     return {"message": f"Job {job_id} cancelled successfully."}
