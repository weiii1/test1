# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 21:16:35 2021
@author: Ivan
版權屬於「行銷搬進大程式」所有，若有疑問，可聯絡ivanyang0606@gmail.com

Line Bot聊天機器人
第一章 Line Bot申請與串接
Line Bot機器人串接與測試
"""
#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('WXJfIVSha2Urij1QZCDXsIDQQAXy5TSJh2hPvOnAgPIbXmt2jLxinW4ezxmOqPoSvzSQDM0OjWv3giTT2UVdVfPt5qzEia9GhW6PXKXzd5i9+Zta2JOrionqkFO3v+TWmMJyX+xtwORUvr5JsoZxcgdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('48e4c8924437e09e4902b5e500f43846')

line_bot_api.push_message('U6384f61cb5051c046ed3e7eab32d21b4', TextSendMessage(text='你可以開始了'))


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

 
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

 
#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    resp = requests.get('https://tw.rter.info/capi.php')
    currency_data = resp.json()
    usd_to_twd = currency_data['USDTWD']['Exrate']
    usd_to_jpy = currency_data['USDJPY']['Exrate']
    usd_to_eur = currency_data['USDEUR']['Exrate']
    usdtwd=float(usd_to_twd)
    usdjpy=float(usd_to_jpy)
    usdeur=float(usd_to_eur)
    twdjpy=usdjpy/usdtwd
    twdeur=usdeur/usdtwd
    message = text=event.message.text
    if re.match('匯率',message):
        buttons_template_message = TemplateSendMessage(
         alt_text='這個看不到',
         template=ButtonsTemplate(
             thumbnail_image_url='https://i.imgur.com/wpM584d.jpg',title='請選擇幣別',text='幣別',
             actions=[
                  MessageAction(
                     label='美元',
                     text='美元匯率'
                 ),
                 MessageAction(
                     label='歐元',
                     text='歐元匯率'
                 ),
                 MessageAction(
                     label='日元',
                     text='日元匯率'
                 ),
             ]
         )
     )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
    elif re.match('美元匯率',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=f'美元 USD 對台幣 TWD：1:{usd_to_twd}'))
    elif re.match('歐元匯率',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=f'台幣 TWD 對歐元 EUR：1:{twdeur}'))
    elif re.match('日元匯率',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=f'台幣 TWD 對日幣 JPY：1:{twdjpy}'))
    #以上為匯率功能#以上為匯率功能#以上為匯率功能#以上為匯率功能#以上為匯率功能#以上為匯率功能
    elif re.match('記帳',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage('老子懶的記'))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage('沒有此指令'))
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)