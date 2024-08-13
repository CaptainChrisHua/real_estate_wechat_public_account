# -*- coding:utf-8 -*-

from apscheduler.schedulers.background import BackgroundScheduler

from src.crontab.tasks import task1, task2

scheduler = BackgroundScheduler(timezone="Asia/Shanghai")

scheduler.add_job(task1, 'cron', day_of_week="*", hour=0, minute=0)  # 每天00:00执行
scheduler.add_job(task2, 'interval', minutes=15, seconds=0)  # 每15分钟执行一次
