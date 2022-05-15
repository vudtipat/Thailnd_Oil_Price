from datetime import datetime
from bs4 import BeautifulSoup
import requests
import schedule
import time
from flask import Flask, request, abort
import json

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

def get_Oil_price():
    url = requests.get("https://www.moneybuffalo.in.th/rate/oil-price")
    soup = BeautifulSoup(url.content, "html.parser")

    data = soup.find("div",{"class":"mb-rate-wrapper oil-wrap"})
    credit_source = data.find("div",{"class":"current-date"})
    print(credit_source.text)
    data = data.find("table",{"class":"oil-table"})
    rows = data.findAll('tr')

    data = []
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
            data.append(tmp)
    print(datetime.now())
    print(data)

schedule.every(5).minutes.do(get_Oil_price)

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def webhook():
    if request.method == 'POST':
        payload = request.json
        Reply_token = payload['events'][0]['replyToken']
        print(Reply_token)
        message = payload['events'][0]['message']['text']
        print(message)
        if 'ดี' in message :
            Reply_messasge = 'ดีมาก'
            ReplyMessage(Reply_token,Reply_messasge,'xzhPj3z8pzT2lEPVN9pKS1oHPNsON9Bn6hm1vqYV6TC5SryjkaW2OD9D5pHsI+OrWOz5hTz970KyeXHzLJYZJ7JUDtf6PkGXRFykLT8QxKHgmBp1RwHhZ4YlatYEsIOqtGm15IWfI6YBcg68+koR6gdB04t89/1O/w1cDnyilFU=') #ใส่ Channel access token
        return request.json, 200
    else:
        abort(400)

def ReplyMessage(Reply_token, TextMessage, Line_Acees_Token):
    LINE_API = 'https://api.line.me/v2/bot/message/reply'
    Authorization = 'Bearer {}'.format(Line_Acees_Token)
    print(Authorization)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization':Authorization
    }
    data = {
        "replyToken":Reply_token,
        "messages":[{
            "type":"text",
            "text":TextMessage
        }]
    }
    data = json.dumps(data)
    r = requests.post(LINE_API, headers=headers, data=data)
    return 200
if __name__ == '__main__':
    app.run(debug=True)
    while(1):
        schedule.run_pending()
        if not schedule.jobs:
            break
        time.sleep(1)


