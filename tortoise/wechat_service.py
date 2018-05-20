# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
import hashlib
import receiver, replyer, tuling
import logging

logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/weixin/", methods = ["GET", "POST"])
def index():
    if request.method == "GET":  # 判断请求方式是GET请求
        logging.info('receive a get request')
        try:
            my_signature = request.args.get('signature')  # 获取携带的signature参数
            my_timestamp = request.args.get('timestamp')  # 获取携带的timestamp参数
            my_nonce = request.args.get('nonce')  # 获取携带的nonce参数
            my_echostr = request.args.get('echostr')  # 获取携带的echostr参数

            token = 'liujinhong'  # 一定要跟刚刚填写的token一致

            # 进行字典排序
            data = [token, my_timestamp, my_nonce]
            data.sort()

            logging.info('data: '+ str(data))

            # 拼接成字符串
            temp = ''.join(data)

            # 进行sha1加密
            mysignature = hashlib.sha1(temp).hexdigest()

            # 加密后的字符串可与signature对比，标识该请求来源于微信
            if my_signature == mysignature:
                logging.info('my_signature == mysignature, success')
                return my_echostr
            else:
                logging.info('my_signature != mysignature, success')
                return ""
        except Exception as e:
            logging.info('get request error: ' + str(e))
            return "error"
    elif request.method == "POST":  # 判断请求方式是POST请求
        logging.info('receive a post request')
        try:
            recData = request.get_data()
            recMsg = receiver.parse_xml(recData)
            if isinstance(recMsg, receiver.Msg):
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                if recMsg.MsgType == 'text':
                    logging.info('this is a text message')
                    t = tuling.Tuling()
                    content = t.get_tuling_response(recMsg.Content)
                    replyMsg = replyer.TextMsg(toUser, fromUser, content)
                    return replyMsg.send()
                if recMsg.MsgType == 'image':
                    logging.info('this is an image message')
                    mediaId = recMsg.MediaId
                    replyMsg = replyer.ImageMsg(toUser, fromUser, mediaId)
                    return replyMsg.send()
                else:
                    return replyer.Msg().send()
            else:
                logging.info('unhandled message type!')
                return replyer.Msg().send()
        except Exception as e:
            logging.info('post request error: ' + str(e))
            return "error"
    else:
        return 'error'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)