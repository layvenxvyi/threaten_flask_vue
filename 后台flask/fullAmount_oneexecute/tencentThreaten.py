#! /usr/bin/python
# -*-coding:utf-8 -*-
# @Time     :   2020-03-09 16:51
# @Author   :   layven

import requests
from saveToExcel import SaveExcel
from lxml import etree
import re

class paramItem(object):
    name=None
    time=None
    urlhref=None
    urldetail=None
    sheetname = u"腾讯云"

class getThreaten_tencent(object):
    def __init__(self):
        self.url='https://cloud.tencent.com/announce/ajax'
        self.headers={'Content-Type': 'application/json; charset=UTF-8'}
        self.totalCount=0
        self.getpage()
        self.items=self.getContent()
        SaveExcel(self.items)

    def getpage(self):
        payload1 = {"action": "getAnnounceList",
                    "data": {"rp": 1, "page": "1", "categorys": ["21"], "labs": [], "keyword": ""}}
        getRes = requests.post(self.url, headers=self.headers, json=payload1)
        self.totalCount = getRes.json()['data']['total']

    def getContent(self):
        items=[]
        name=[]
        time=[]
        urlhref=[]
        urldetail=[]
        item = paramItem()
        payload2 = {"action": "getAnnounceList",
                    "data": {"rp": self.totalCount, "page": "1", "categorys": ["21"], "labs": [], "keyword": ""}}
        '''
        腾讯云这边的请求直接通过rp参数中设置为所有条目，第一个页面最多可返回100，其他的不要了，太久远，只需请求一次url可得到所有公告数据，再把得到的属性值赋值
        '''
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
        items.append(item)
        return items

if __name__=='__main__':
    getThreaten_tencent()