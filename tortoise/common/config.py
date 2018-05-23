# -*- coding: utf-8 -*-
import os

# wechat config
AppID = 'wx2b1af66c1c59e9c2'

AppSecret = '35061c49ec1fabe2d36c6191c5a188c7'

# tuling config
TulingUrl = 'http://www.tuling123.com/openapi/api'

TulingKey = '44f40f88a9ea497e8b073ca6bbcc8ac2'


tortoise_home = os.path.abspath(os.path.dirname(__file__) + '/..')

sqlitedb_path = tortoise_home + '/tortoise.db'

access_token_table = 'access_token'

