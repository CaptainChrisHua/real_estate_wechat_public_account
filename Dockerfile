FROM python:3.9.12-slim-buster

MAINTAINER Chris "chris.weihaohua@gmail.com"

ENV LANG=C.UTF-8

RUN ln -fs /usr/share/zoneinfo/America/Los_Angeles /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

COPY requirements.txt requirements.txt

RUN mkdir /logs /logs/project_name && pip3 install --no-cache -r requirements.txt

COPY . /wechat_fastapi
WORKDIR /wechat_fastapi

ENV PYTHONPATH=/projects/wechat_fastapi

EXPOSE ${APP_PORT}

ENTRYPOINT gunicorn -k uvicorn.workers.UvicornWorker -b 0.0.0.0:{APP_PORT} -c gunicorn.conf.py app:app --access-logformat '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'
