# -*- coding:utf-8 -*-
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from src.crontab.tasks import refresh_access_token, task2

# scheduler.add_job(task1, 'cron', day_of_week="*", hour=0, minute=0)  # 每天00:00执行
# scheduler.add_job(task2, 'interval', minutes=15, seconds=0)  # 每15分钟执行一次

scheduler = AsyncIOScheduler()
scheduler.add_job(refresh_access_token, IntervalTrigger(hours=2))
