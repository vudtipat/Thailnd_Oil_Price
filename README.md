# Thailnd_Oil_Price

USESAGE
    - HEROKU use to deploy bot-server
    - Line developer use to make message api to make bot server
    - Ngrok use to forwand port to use local server to public 

REFERENCE
    - https://developers.line.biz/flex-simulator/ use to design flex to send to line
    - https://github.com/line/line-bot-sdk-python use to see the document and example of line developer sdk
    - https://www.moneybuffalo.in.th/rate/oil-price use to see reference oil price by web scraping
    - https://medium.com/linedevth/ปฐมบทการสร้าง-line-bot-b2cb90643901 use to reference to create line channel bot


Command 
    - Deploy to heroku
        git push heroku HEAD:master (from hero branch)
    - Ngrok to forwand port ($port = port number)
        ngrok http $port
    
