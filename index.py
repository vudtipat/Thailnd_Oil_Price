from datetime import datetime
from bs4 import BeautifulSoup
import requests
import schedule
import time

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

while(1):
    schedule.run_pending()
    if not schedule.jobs:
        break
    time.sleep(1)
