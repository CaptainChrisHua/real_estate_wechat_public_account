# -*- coding:utf-8 -*-
import requests

from config.config import PUB_APP_ID, PUB_APP_SECRET


def get_access_token():
    url = "https://api.weixin.qq.com/cgi-bin/token"
    params = {
        "grant_type": "client_credential",
        "appid": PUB_APP_ID,
        "secret": PUB_APP_SECRET
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        print(data["access_token"])
        return data["access_token"]
