# -*- coding: utf-8 -*-#
import json
import requests
import logging

logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

url = 'http://www.tuling123.com/openapi/api'
KEY = '44f40f88a9ea497e8b073ca6bbcc8ac2'

class Tuling:
    def __init__(self):
        self

    def get_tuling_response(self, message):
        logger.info('get a tuling request, the message is: ' + str(message))

        try:
            headers = {'Content-type': 'text/html', 'charset': 'utf-8'}
            query = {'key':KEY, 'info':message.encode('utf-8')}
            r = requests.get(url, params=query, headers=headers)
            r.encoding = 'utf-8'
            return json.loads(r.text).get('text').replace('<br>', '\n')
        except Exception as e:
            logging.info('tuling error info: ' + str(e))
            return '谢谢关注Symblic'


if __name__ == '__main__':
    t = Tuling()
    data = t.get_tuling_response("hello")