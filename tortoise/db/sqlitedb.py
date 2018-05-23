# -*- coding: utf-8 -*-
import sqlite3
from common import config

class TortoiseDB:
    def __init__(self):
        conn = self.get_conn()
        self.create_access_token_table(conn)
        conn.close()

    def get_conn(self):
        conn = sqlite3.connect(config.sqlitedb_path)
        conn.row_factory = sqlite3.Row
        return conn

    def create_access_token_table(self, conn):
        cur = conn.cursor()
        cur.execute('''SELECT * FROM sqlite_master WHERE type="table" AND name=?''', (config.access_token_table,))
        rows = cur.fetchall()

        if len(rows) == 0:
            cur.execute(
                'CREATE TABLE `%s`'
                '(token text, expires_in INT, get_token_time TIMESTAMP) ' % config.access_token_table)
        conn.commit()

    def get_access_token(self, conn):
        cur = conn.cursor()
        cur.execute('select token, expires_in, get_token_time from `%s`' % config.access_token_table)
        rows = cur.fetchall()
        if len(rows) != 0:
            return rows[0]
        return None

    def put_access_token(self, conn, token, expires_in, time):
        cur = conn.cursor()
        cur.execute('delete from `%s`' % config.access_token_table)
        cur.execute('insert into `%s` (`token`, `expires_in`, `get_token_time`)'
                  'values (?, ?, ?)' % config.access_token_table, (token, expires_in, time))
        conn.commit()
