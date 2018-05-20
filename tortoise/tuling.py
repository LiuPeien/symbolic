# -*- coding: utf-8 -*-#
import json
import requests

url = 'http://www.tuling123.com/openapi/api'
KEY = '44f40f88a9ea497e8b073ca6bbcc8ac2'

class Tuling:
    def __init__(self):
        self

    def get_tuling_response(self, message):

        headers = {'Content-type': 'application/json'}

        query = {'key':KEY, 'info':message}

        r = requests.get(url, params=query, headers=headers)

        res = r.text

        return json.loads(res).get('text').replace('<br>', '\n')


if __name__ == '__main__':
    t = Tuling()
    data = t.get_tuling_response("hello")