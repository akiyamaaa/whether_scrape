#ライブラリのインポート
import requests
from bs4 import BeautifulSoup
import smtplib, ssl
from email.mime.text import MIMEText

#tenki.jpの目的の地域のページのURL
url = 'https://tenki.jp/forecast/5/25/5040/22130/'

#HTTPリクエスト
r = requests.get(url)

#HTMLの解析
bsObj = BeautifulSoup(r.content, "html.parser")

#今日の天気を取得
today = bsObj.find(class_="today-weather")
weather = today.p.string

#気温情報のまとまり
temp=today.div.find(class_="date-value-wrap")

#降水確率のまとまり
rain = today.find(class_="precip-table")

#気温の取得
temp=temp.find_all("dd")
temp_max = temp[0].span.string #最高気温
temp_max_diff=temp[1].string #最高気温の前日比
temp_min = temp[2].span.string #最低気温
temp_min_diff=temp[3].string #最低気温の前日比

#降水確率の取得
rain = rain.find_all("td")
rain_0_6 = rain[0].text
rain_6_12 = rain[1].text
rain_12_18 = rain[2].text
rain_18_24 = rain[3].text

#降水確率判別
def judge_rain(rain_flag):
    if(rain_flag != "---"):
        rain_flag = rain_flag.split("%")
        num = int(rain_flag[0])
        if (num >= 70):
            return 1
    return 0

rain06 = judge_rain(rain_0_6)
rain612 = judge_rain(rain_6_12)
rain1218 = judge_rain(rain_12_18)
rain1824 = judge_rain(rain_18_24)

if (rain612 == 1):
    subject = "朝だけ降るんご"
    if (rain1218 == 1):
        subject = "夕方には止むけど、朝雨降るかもよ。"
        if(rain1824 == 1):
            subject = "1日中降るよ。"
    elif (rain1218 == 0):
        subject = "夕方には止むけど、朝雨降るかもよ。"
        if(rain1824 == 1):
            subject = "朝降って夕方止んで夜降るよ。"

if (rain612 == 0):
    subject = "朝は降らない。"
    if (rain1218 == 1):
        subject = "夕方だけ降るよ"
        if(rain1824 == 1):
            subject = "夕方夜降るよ"
    elif (rain1218 == 0):
        subject = "1日降らないよ"
        if(rain1824 == 1):
            subject = "夜だけ降るよ"

# ファイルに書き込み
f = open('whether.txt','w')

f.write("天気:{}\n".format(weather))
f.write("最高気温:{}\n".format(temp_max,temp_max_diff))
f.write("最低気温:{}\n".format(temp_min,temp_min_diff))
f.write("降水確率 0~6:{}\n".format(rain_0_6))
f.write("降水確率 6~12:{}\n".format(rain_6_12))
f.write("降水確率 12~18:{}\n".format(rain_12_18))
f.write("降水確率 18~24:{}\n".format(rain_18_24))

f.close()

f = open('whether.txt','r')

f_msg = f.read()

f.close()