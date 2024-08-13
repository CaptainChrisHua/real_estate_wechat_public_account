# -*- coding:utf-8 -*-

import os
from configparser import ConfigParser
from pathlib import Path

BASE_DIR = Path(os.path.realpath(__file__)).parent.parent.parent  # 根目录
DATA_DIR = BASE_DIR.joinpath('data')
prop_file = BASE_DIR.joinpath('config/prop.conf')

config = {}
prop_config = ConfigParser()
prop_config.read(prop_file, encoding="utf-8")
prop_config = dict(prop_config.items(raw=True))
for key in prop_config:
    prop_config[key] = dict(prop_config[key])
config.update(prop_config)
