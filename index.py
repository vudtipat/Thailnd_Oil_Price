from datetime import datetime
from bs4 import BeautifulSoup
import requests
import schedule
import time
from flask import Flask, request, abort
import json
import os
import sys
from argparse import ArgumentParser
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    MemberJoinedEvent, MemberLeftEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton,
    ImageSendMessage)
label = {   
            "HPDS.jpg":"ไฮพรีเมียมดีเซล",
            "HidieselSb7.jpg":"ไฮดีเซล B7",
            "HidieselSm.jpg":"ไฮดีเซล",
            "HidieselSb20.jpg":"ไฮดีเซล B20",
            "E85evoWeb2-76.jpg":"แก๊สโซฮอล E85",
            "E20evoWeb2-76.jpg":"แก๊สโซฮอล E20",
            "GSH91evoWeb2-76.jpg":"แก๊สโซฮอล 91",
            "GSH95evoWeb2-76.jpg":"แก๊สโซฮอล 95",
            "oil-ngv.png":""
        }

credit = ""
datasource = []
def get_Oil_price():
    global credit,datasource
    url = requests.get("https://www.moneybuffalo.in.th/rate/oil-price")
    soup = BeautifulSoup(url.content, "html.parser")

    data = soup.find("div",{"class":"mb-rate-wrapper oil-wrap"})
    credit_s = data.find("div",{"class":"current-date"})
    credit = credit_s.text
    print(credit_s.text)
    data = data.find("table",{"class":"oil-table"})
    rows = data.findAll('tr')

    for element in rows[1:]:
        tmp = []
        # img,todayPrince,tomorrowPrice
        tm = element.find('td')
        tmp.append(label[tm.findChild('img')['src'].split('/')[-1]])
        for lsts in element.findAll('td'):
            if( lsts.text != ''):
                tmp.append(lsts.text)
        #print(tmp)
        if(len(tmp) > 1):
            datasource.append(tmp)
    print(datasource)

schedule.every(5).minutes.do(get_Oil_price)

app = Flask(__name__)

channel_secret = ""
channel_access_token = ""
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@app.route("/test", methods=['POST'])
def testbroadcast():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print("Request body: " + body)

    try:
        line_bot_api.broadcast(TextSendMessage(text='Hello World!'))
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    print("message")
    msg = str(event.message.text)
    print(msg)

    #region get profile
    profile = line_bot_api.get_profile(event.source.user_id)
    print(profile)
    #endregion
    if("ราคาน้ำมัน" in msg):
        flex_str = """
        {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "ราคาน้ำมัน",
                    "weight": "bold",
                    "size": "3xl",
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": "%s",
                    "size": "xs",
                    "color": "#aaaaaa",
                    "wrap": true
                },
                {
                    "type": "separator",
                    "margin": "xxl"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "xxl",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": "ไฮพรีเมียมดีเซล",
                            "size": "sm",
                            "color": "#555555",
                            "flex": 0
                        },
                        {
                            "type": "text",
                            "text": "(วันนี้)฿%.2f",
                            "size": "sm",
                            "color": "#111111",
                            "align": "end"
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": "(พรุ่งนี้)฿%.2f",
                            "size": "sm",
                            "color": "#54A42C",
                            "align": "end"
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": "ไฮดีเซล B7",
                            "size": "sm",
                            "color": "#555555",
                            "flex": 0
                        },
                        {
                            "type": "text",
                            "text": "฿%.2f",
                            "size": "sm",
                            "color": "#111111",
                            "align": "end"
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": "฿%.2f",
                            "size": "sm",
                            "color": "#54A42C",
                            "align": "end"
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": "ไฮดีเซล",
                            "size": "sm",
                            "color": "#555555",
                            "flex": 0
                        },
                        {
                            "type": "text",
                            "text": "฿%.2f",
                            "size": "sm",
                            "color": "#111111",
                            "align": "end"
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": "฿%.2f",
                            "size": "sm",
                            "color": "#54A42C",
                            "align": "end"
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": "ไฮดีเซล B20",
                            "size": "sm",
                            "color": "#555555"
                        },
                        {
                            "type": "text",
                            "text": "฿%.2f",
                            "size": "sm",
                            "color": "#111111",
                            "align": "end"
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": "฿%.2f",
                            "size": "sm",
                            "color": "#54A42C",
                            "align": "end"
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": "แก๊สโซฮอล E85",
                            "size": "sm",
                            "color": "#555555"
                        },
                        {
                            "type": "text",
                            "text": "฿%.2f",
                            "size": "sm",
                            "color": "#111111",
                            "align": "end"
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": "฿%.2f",
                            "size": "sm",
                            "color": "#54A42C",
                            "align": "end"
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": "แก๊สโซฮอล E20",
                            "size": "sm",
                            "color": "#555555"
                        },
                        {
                            "type": "text",
                            "text": "฿%.2f",
                            "size": "sm",
                            "color": "#111111",
                            "align": "end"
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": "฿%.2f",
                            "size": "sm",
                            "color": "#54A42C",
                            "align": "end"
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": "แก๊สโซฮอล 91",
                            "size": "sm",
                            "color": "#555555"
                        },
                        {
                            "type": "text",
                            "text": "฿%.2f",
                            "size": "sm",
                            "color": "#111111",
                            "align": "end"
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": "฿%.2f",
                            "size": "sm",
                            "color": "#54A42C",
                            "align": "end"
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": "แก๊สโซฮอล 95",
                            "size": "sm",
                            "color": "#555555"
                        },
                        {
                            "type": "text",
                            "text": "฿%.2f",
                            "size": "sm",
                            "color": "#111111",
                            "align": "end"
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": "฿%.2f",
                            "size": "sm",
                            "color": "#54A42C",
                            "align": "end"
                        }
                        ]
                    }
                    ]
                }
                ]
            },
            "styles": {
                "footer": {
                "separator": true
                }
            }
        }
        """%(credit,float(datasource[0][1]),float(datasource[0][2]),float(datasource[1][1]),float(datasource[1][2]),float(datasource[2][1]),float(datasource[2][2]),float(datasource[3][1]),float(datasource[3][2]),float(datasource[4][1]),float(datasource[4][2]),float(datasource[5][1]),float(datasource[5][2]),float(datasource[6][1]),float(datasource[6][2]),float(datasource[7][1]),float(datasource[7][2]))
        print(credit)
        message = FlexSendMessage(alt_text="hello", contents=json.loads(flex_str))
        line_bot_api.reply_message(
            event.reply_token,
            message
        ) 
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )

port = int(os.environ.get("PORT", 5000))
if __name__ == '__main__':
    get_Oil_price()
    app.run(host='0.0.0.0', port=port, debug=True)
    while(1):
        schedule.run_pending()
        if not schedule.jobs:
            break
        time.sleep(1)


