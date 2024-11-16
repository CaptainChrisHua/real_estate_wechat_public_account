# -*- coding:utf-8 -*-

from src.conf import config

LOG_PATH = config["log"]["log_path"]

LOG_LEVEL = config["log"]["log_level"]

TRACE_TYPE = config["trace"]["type"]

TRACE_PARAM = config["trace"]["param"]

# MONGODB_CRAWLER = config["mongodb-crawler"]
#
# MYSQL_HADOOP_DB = config["mysql-hadoop_db"]
#
# MYSQL_WORD_RECOMMEND_DB = config["mysql-word_recommend_db"]
#
# REDIS_ALGORITHMS = config["redis-algorithms"]
#
# REDIS_REPORT = config["redis-report"]
#
# ENV = config["global"]["env"]


PUB_APP_ID = "wx659ed80cbfcace91"
PUB_APP_SECRET = "785f3ac5d7aa0d466f2314d4d7a64d2b"
PUB_APP_TOKEN = "CaliforniaRealEstate"
# PUB_APP_TOKEN = "wx44"
AES_KEY = "nOGRgjqdZAGL6XGNDfvhD75KJaVuisZ2A6YZbEVGz1Q"
# ACCESS_TOKEN = "83_3PXHhWqxVS9hZD-PwhKqZY3NTIl_x7YzVr8z0UrlptDCFVdkG_K83YaUkacbNTFAd1HQ8AUkKQQp6gxgMrFYhjRC3GsaBmg3Ykj9idach27eYt8kKEprdQAPQzELTUhAFAVDE"

REDIS = {
    'host': '127.0.0.1',
    'port': 6666,
    'db': 6,
    'password': 'chris'
}

