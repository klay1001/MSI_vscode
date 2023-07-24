from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.models import TemplateSendMessage, ButtonsTemplate, MessageAction


import configparser

import random
新莊=["泰99","蒙古烤肉","名廚鐵板燒","茶之鄉","築間","忠青商行","薩利亞","燒肉smile","後港一路蛋炒飯"]
台北=["Lisa泰式料理","印度皇宮","忠青商行","薩利亞","士林石二鍋","寧夏雞肉飯","大稻埕鐵板炒麵","西門天婦羅"]
新竹=["車庫鹽酥雞","排骨奶奶","馬辣","森森燒肉","黃悶雞米飯","TGB很牛排","桃太郎燒肉"]

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))


# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        print(body, signature)
        handler.handle(body, signature)
        
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def pretty_echo(event):
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        # 檢查收到的訊息是否是 "吃飯"
        if event.message.text == "吃飯":

            # 設定按鈕模板訊息
            buttons_template = TemplateSendMessage(
                alt_text='選擇餐廳地點',
                template=ButtonsTemplate(
                    text='在哪裡吃飯呢?',
                    actions=[
                        MessageAction(label='台北', text='台北'),
                        MessageAction(label='新莊', text='新莊'),
                        MessageAction(label='新竹', text='新竹')
                    ]
                )
            )
            # 回覆按鈕訊息給使用者
            line_bot_api.reply_message(
                event.reply_token,
                buttons_template
            )

        elif event.message.text in ["台北", "新莊", "新竹"]:
            place = event.message.text
            if place == "台北":
                chosen_place = 台北
            elif place == "新莊":
                chosen_place = 新莊
            elif place == "新竹":
                chosen_place = 新竹

            if chosen_place:
                random_element = random.choice(chosen_place)
                # 回覆選擇的餐廳名稱給使用者
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="就決定吃：" + random_element)
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage("無此地區列表")
                )
                
            
if __name__ == "__main__":
    app.run()
