#! /usr/bin/python
# -*-coding:utf-8 -*-
# @Time     :   2020-03-09 16:51
# @Author   :   layven
import requests
from lxml import etree
import re

class paramItem(object):
    name=None
    time=None
    urlhref=None
    urldetail=None
    origin = 2#2=腾讯云
    now_totalCount=None

def getpage():
    payload1 = {"action": "getAnnounceList",
                "data": {"rp": 1, "page": "1", "categorys": ["21"], "labs": [], "keyword": ""}}
    getRes = requests.post('https://cloud.tencent.com/announce/ajax', headers={'Content-Type': 'application/json; charset=UTF-8'}, json=payload1)
    totalCount = getRes.json()['data']['total']
    return totalCount

class getThreaten_tencent(object):
    def __init__(self):
        self.url='https://cloud.tencent.com/announce/ajax'
        self.headers={'Content-Type': 'application/json; charset=UTF-8'}
        self.items=self.getContent()

    def getContent(self):
        items=[]
        name=[]
        time=[]
        urlhref=[]
        urldetail=[]
        item = paramItem()
        payload2 = {"action": "getAnnounceList",
                    "data": {"rp": 10, "page": "1", "categorys": ["21"], "labs": [], "keyword": ""}}
        getContent = requests.post(self.url, headers=self.headers, json=payload2)
        Init = getContent.json()['data']['rows']
        for i in Init:
            item.urlhref=urlhref.append('https://cloud.tencent.com/announce/detail/' + str(i['announceId']))
            name.append(i['title'])
            time.append(i['addTime'])
        for j in urlhref:
            getContent2 = requests.get(j)
            html = etree.HTML(getContent2.text)
            subtitle = html.xpath('//h2//text()')
            detail = html.xpath("//div[@class='msg-d-wrap']//text()")
            resstr = ""
            for text in detail:
                newtext = str(text).strip().replace(u'\xa0', "").replace(u" ", "")
                if newtext.startswith(u"【"):
                    resstr += "\n" + newtext
                else:
                    resstr += newtext
            for subone in subtitle:#改进内容排版的小标题不以【】开头的
                resstr=re.sub(subone,'\n'+subone+'：',resstr)
            urldetail.append(resstr)
        item.name=name
        item.time=time
        item.urlhref=urlhref
        item.urldetail=urldetail
        item.now_totalCount=getpage()
        items.append(item)
        return items