from sqlitedb import TortoiseDB
import urllib
import time
import json
import config
import datetime

class Token:
    def __init__(self):
        self.db = TortoiseDB()
        self.url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential"

    def get_access_token_formdb(self):
        conn = self.db.get_conn()
        access_token = self.db.get_access_token(conn)
        return access_token


    def real_get_access_token(self):
        postUrl = (self.url + "&appid=%s&secret=%s" % (config.AppID, config.AppSecret))
        urlResp = urllib.urlopen(postUrl)
        urlResp = json.loads(urlResp.read())

        access_token = urlResp['access_token']
        expires_in = urlResp['expires_in']
        cur_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn = self.db.get_conn()
        self.db.put_access_token(conn, access_token, expires_in, cur_time)
        conn.close()

        return access_token


    def get_fresh_access_token(self):
        db_res = self.get_access_token_formdb()

        if db_res is None:
            access_token = self.real_get_access_token()
            return access_token
        else:
            access_token = db_res[0]
            expires_in = db_res[1]
            insert_time = db_res[2]
            insert_time_sec = time.mktime(time.strptime(insert_time, '%Y-%m-%d %H:%M:%S'))
            cur_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cur_time_sec = time.mktime(time.strptime(cur_time, '%Y-%m-%d %H:%M:%S'))

            if cur_time_sec - insert_time_sec > expires_in - 100:
                access_token = self.real_get_access_token()

            return access_token