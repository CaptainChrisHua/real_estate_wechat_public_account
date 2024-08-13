# -*- coding:utf-8 -*-
# 监听内网端口
# bind = '0.0.0.0:9005'

# 并行工作进程数
workers = 1

worker_class = 'uvicorn.workers.UvicornH11Worker'
# 指定每个工作者的线程数
# threads = 1

# 设置守护进程
# daemon = 'False'

# 工作模式协程
# worker_class = 'gevent'

# worker超时时间
timeout = 600

# 设置最大并发量
# worker_connections = 1000

# 设置进程文件目录
# pidfile = './run/gunicorn.pid'

# 设置访问日志和错误信息日志路径
accesslog = './data/logs/access.log'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'
errorlog = './data/logs/access_error.log'
# 设置日志记录水平
loglevel = 'info'

