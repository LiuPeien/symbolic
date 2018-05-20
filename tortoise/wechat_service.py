# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
import hashlib
import receiver, replyer, tuling

app = Flask(__name__)


@app.route("/weixin/", methods = ["GET", "POST"])
def index():
    if request.method == "GET":  # 判断请求方式是GET请求
        try:
            my_signature = request.args.get('signature')  # 获取携带的signature参数
            my_timestamp = request.args.get('timestamp')  # 获取携带的timestamp参数
            my_nonce = request.args.get('nonce')  # 获取携带的nonce参数
            my_echostr = request.args.get('echostr')  # 获取携带的echostr参数

            token = 'liujinhong'  # 一定要跟刚刚填写的token一致

            # 进行字典排序
            data = [token, my_timestamp, my_nonce]
            data.sort()

            # 拼接成字符串
            temp = ''.join(data)

            # 进行sha1加密
            mysignature = hashlib.sha1(temp).hexdigest()

            # 加密后的字符串可与signature对比，标识该请求来源于微信
            if my_signature == mysignature:
                return my_echostr
            else:
                return ""
        except Exception as e:
            return "error"
    elif request.method == "POST":  # 判断请求方式是GET请求
        try:
            recData = request.get_data()
            recMsg = receiver.parse_xml(recData)
            if isinstance(recMsg, receiver.Msg):
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                if recMsg.MsgType == 'text':
                    t = tuling.Tuling()
                    content = t.get_tuling_response(recMsg.Content)
                    replyMsg = replyer.TextMsg(toUser, fromUser, content)
                    return replyMsg.send()
                if recMsg.MsgType == 'image':
                    mediaId = recMsg.MediaId
                    replyMsg = replyer.ImageMsg(toUser, fromUser, mediaId)
                    return replyMsg.send()
                else:
                    return replyer.Msg().send()
            else:
                print
                "暂且不处理"
                return replyer.Msg().send()
        except Exception as e:
            return "error"
    else:
        return 'error'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)