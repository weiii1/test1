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
from flask import Flask, request, abort,jsonify

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)
import re
import requests
import os, sys,json
cities = ['基隆市','嘉義市','臺北市','嘉義縣','新北市','臺南市','桃園縣','高雄市','新竹市','屏東縣','新竹縣','臺東縣','苗栗縣','花蓮縣','臺中市','宜蘭縣','彰化縣','澎湖縣','南投縣','金門縣','雲林縣','連江縣']
ww=1
# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('WXJfIVSha2Urij1QZCDXsIDQQAXy5TSJh2hPvOnAgPIbXmt2jLxinW4ezxmOqPoSvzSQDM0OjWv3giTT2UVdVfPt5qzEia9GhW6PXKXzd5i9+Zta2JOrionqkFO3v+TWmMJyX+xtwORUvr5JsoZxcgdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('48e4c8924437e09e4902b5e500f43846')

line_bot_api.push_message('U6384f61cb5051c046ed3e7eab32d21b4', TextSendMessage(text='你可以開始了'))
def get(city):
    token = 'CWB-B0A62AE7-CF1D-4C83-BF46-7E082EF1FC9A'
    url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=' + token + '&format=JSON&locationName=' + str(city)
    Data = requests.get(url)
    Data = (json.loads(Data.text,encoding='utf-8'))['records']['location'][0]['weatherElement']
    res = [[] , [] , []]
    for j in range(3):
        for i in Data:
            res[j].append(i['time'][j])
    return res

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
    usd_to_krw = currency_data['USDKRW']['Exrate']
    usd_to_cny = currency_data['USDCNY']['Exrate']
    usdtwd=float(usd_to_twd)
    usdjpy=float(usd_to_jpy)
    usdeur=float(usd_to_eur)
    usdkrw=float(usd_to_krw)
    usdcny=float(usd_to_cny)
    twdjpy=usdjpy/usdtwd
    twdeur=usdeur/usdtwd
    twdkrw=usdkrw/usdtwd
    twdcny=usdcny/usdtwd
    twdusd=1/usdtwd
    twdjpy=(round(twdjpy,5))
    twdeur=(round(twdeur,5))
    twdcny=(round(twdcny,5))
    ss= event.message.text 
    message = event.message.text
 
    if re.match('匯率',message):
        buttons_template_message = TemplateSendMessage(
         alt_text='這是LineBot',
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
                 MessageAction(
                     label='人民幣',
                     text='人民幣匯率'
                 )
             ]
         )
     )
    # elif re.match('美元匯率',message):
    #     Confirm_template = TemplateSendMessage(
    #     alt_text='目錄 template',
    #     template=ConfirmTemplate(
    #         title='這是ConfirmTemplateaaaaaa',
    #         text='adasdasds用於兩種按鈕選擇bbbb',
    #         actions=[                              
    #             MessageTemplateAction(
    #                 label='台幣美金',
    #                 text='請輸入兌換之台幣金額'
    #             ),
    #             MessageTemplateAction(
    #                 label='美金台幣',
    #                 text='請輸入兌換之美金金額'
    #             )
    #         ]
    #     )
    # )
    #     line_bot_api.reply_message(event.reply_token,Confirm_template)
    elif re.match('歐元匯率',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=f'台幣 TWD 對歐元 EUR：1:{twdeur}'))
    elif re.match('日元匯率',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=f'台幣 TWD 對日幣 JPY：1:{twdjpy}'))
    elif re.match('韓元匯率',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=f'台幣 TWD 對韓元 KRW：1:{twdkrw}'))
    elif re.match('人民幣匯率',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=f'台幣 TWD 對人民幣 CNY：1:{twdcny}'))
    #以上為匯率功能#以上為匯率功能#以上為匯率功能#以上為匯率功能#以上為匯率功能#以上為匯率功能
    elif re.match('記帳功能',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage('老子懶的記'))
    elif re.match('翻譯功能',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage('老子懶的記'))
    elif re.match('查詢天氣功能',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage('請輸入城市名稱'))
        print(message)
    elif (ss in cities):
       # line_bot_api.reply_message(event.reply_token,TextSendMessage('aaaaa12332233'))
        reply_token = event.reply_token
        city = ss
        city = city.replace('台','臺')
        print(city)
        res=get(city)
        line_bot_api.reply_message(reply_token, TemplateSendMessage(
    alt_text = city + '未來 36 小時天氣預測',
    template = CarouselTemplate(
        columns = [
            CarouselColumn(
                thumbnail_image_url = 'https://i.imgur.com/Ex3Opfo.png',
                title = '{} ~ {}'.format(res[0][0]['startTime'][5:-3],res[0][0]['endTime'][5:-3]),
                text = '天氣狀況 {}\n溫度 {} ~ {} °C\n降雨機率 {}'.format(data[0]['parameter']['parameterName'],data[2]['parameter']['parameterName'],data[4]['parameter']['parameterName'],data[1]['parameter']['parameterName']),
                actions = [
                    URIAction(
                        label = '詳細內容',
                        uri = 'https://www.cwb.gov.tw/V8/C/W/County/index.html'
                    )
                ]
            )for data in res
        ]
    )
   ))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage('沒有此指令'))

    
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)