# coding=utf-8
import requests
import re
import json
import time
import pandas as pd

def ADDINFO(file,df,time):
    #df.to_csv(file,index=0,header=0,mode="a")
    try:
        df2 = pd.read_csv(file,header=0,encoding = 'gbk',engine ='python',usecols=['时间'])#，usecols=['时间']
        if df2.iloc[df2.shape[0]-1,0] != time:
            df.to_csv(file,index=0,header=0,mode="a")
            print("Add..")
            
    except:
        print("Create",file)
        df.to_csv(file,index=0)
    


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'Host':'sa.sogou.com',
    'Referer':'https://www.sogou.com/tx?hdq=sogou-wsse-3f7bcd0b3ea82268&ie=utf-8&query=%E7%96%AB%E6%83%85',
}
url = "http://sa.sogou.com/new-weball/page/sgs/epidemic"

text = requests.get(url,headers=headers)
text = text.content.decode()
#处理字符串
text2 = 'window.__INITIAL_STATE__ ='
text = text.split(text2)[1]
text2 = '</script>'
text = text.split(text2)[0]
text = json.loads(text)
info = text["data"]
domInfo = {}
ShanghaiInfo = {}
HubeiInfo = {}
#全国情况
#print(info['domesticStats'])
timeStamp = info['domesticStats']['timestamp']
#print(timeStamp)
timeStamp = str(timeStamp)[0:-3]
timeArray = time.localtime(int(timeStamp))
otherStyleTime = time.strftime("%Y.%m.%d %H:%M:%S", timeArray)
print("全国情况：{}\t确诊人数:{}\t疑似人数:{}\t治愈人数:{}\t死亡人数:{}".format(
    otherStyleTime,
    info['domesticStats']['diagnosed'],
    info['domesticStats']['suspect'],
    info['domesticStats']['cured'],
    info['domesticStats']['death']))
domInfo["时间"] = otherStyleTime
domInfo["全国确诊"] = [info['domesticStats']['diagnosed']]
domInfo["全国疑似"] = [info['domesticStats']['suspect']]
domInfo["全国治愈"] = [info['domesticStats']['cured']]
domInfo["全国死亡"] = [info['domesticStats']['death']]
#城市信息
areaInfo = info["area"]
for province in areaInfo:
    #print(province.keys())
    try:
        print("{}:\t确诊人数:{}\t疑似人数:{}\t治愈人数:{}\t死亡人数:{}".format(
            province['provinceName'],
            province['confirmedCount'],
            province['suspectedCount'],
            province['curedCount'],
            province['deadCount']))
        domInfo[province['provinceName']+"确诊"] = [province['confirmedCount']]
        domInfo[province['provinceName']+"疑似"] = [province['suspectedCount']]
        domInfo[province['provinceName']+"治愈"] = [province['curedCount']]
        domInfo[province['provinceName']+"死亡"] = [province['deadCount']]
    except:
        print(province['provinceName'],"信息缺失..")
    
    if province['provinceName'] == '上海':
        ShanghaiInfo["时间"] = otherStyleTime
        for area in province['cities']:
            print("--\t{}\t确诊人数:{}\t疑似人数:{}\t治愈人数:{}\t死亡人数:{}".format(
                area['cityName'],
                area['confirmedCount'],
                area['suspectedCount'],
                area['curedCount'],
                area['deadCount']))
            ShanghaiInfo[area['cityName']+"确诊"] = [area['confirmedCount']]
            ShanghaiInfo[area['cityName']+"疑似"] = [area['suspectedCount']]
            ShanghaiInfo[area['cityName']+"治愈"] = [area['curedCount']]
            ShanghaiInfo[area['cityName']+"死亡"] = [area['deadCount']]
            
    if province['provinceName'] == '湖北':
        HubeiInfo["时间"] = otherStyleTime
        for area in province['cities']:
            print("--\t{}\t确诊人数:{}\t疑似人数:{}\t治愈人数:{}\t死亡人数:{}".format(
                area['cityName'],
                area['confirmedCount'],
                area['suspectedCount'],
                area['curedCount'],
                area['deadCount']))
            HubeiInfo[area['cityName']+"确诊"] = [area['confirmedCount']]
            HubeiInfo[area['cityName']+"疑似"] = [area['suspectedCount']]
            HubeiInfo[area['cityName']+"治愈"] = [area['curedCount']]
            HubeiInfo[area['cityName']+"死亡"] = [area['deadCount']]    
    

domDf = pd.DataFrame(data=domInfo)
ShDf = pd.DataFrame(data=ShanghaiInfo)
HubeiDf = pd.DataFrame(data=HubeiInfo)
#print(domDf)
#print(ShDf)
#domDf.to_csv("全国情况统计.csv",index=0)
#ShDf.to_csv("sh情况统计.csv",index=0)

ADDINFO("全国情况统计.csv",domDf,otherStyleTime)
ADDINFO("上海情况统计.csv",ShDf,otherStyleTime)
ADDINFO("湖北情况统计.csv",HubeiDf,otherStyleTime)




