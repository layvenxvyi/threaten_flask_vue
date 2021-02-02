#! /usr/bin/python
# -*-coding:utf-8 -*-
# @Time     :   2020-03-04 18:24
# @Author   :   layven
import requests
from lxml import etree

class paramItem(object):
    name=None
    time=None
    urlhref=None
    urldetail=None
    origin=1#1=阿里云
    now_totalCount=None

def getTotalCount():
    totalCount=[]
    getContent = requests.get('https://help.aliyun.com/notice_list_page/9213612/1.html')
    html = etree.HTML(getContent.text)
    date=html.xpath("//ul/li/span[@class='y-right']/text()")
    time=html.xpath("//ul/li//span[@class='time']/text()")
    for i in range(len(date)):
        totalCount.append(date[i]+' '+time[i])# 设置目前的时间为标准线
    # page = html.xpath("//script[last()]/text()")
    # string1 = str(page[0])#转换类型string
    # list1= string1.split(":")#取值处理
    # totalCount = int(list1[1].split(",")[0])#获取总条数
    return totalCount

class getThreaten_ali(object):
    def __init__(self):
        self.url='https://help.aliyun.com/notice_list_page/9213612/1.html'
        self.items=self.getContent()

    def getContent(self):
        items=[]
        item=paramItem()#实例化为对象item
        getContent = requests.get(self.url)
        # print getContent.text
        html = etree.HTML(getContent.text)
        item.name = html.xpath("//ul/li/a/text()")#赋予属性值
        item.time=[]
        date = html.xpath("//ul/li/span[@class='y-right']/text()")
        time = html.xpath("//ul/li//span[@class='time']/text()")
        for i in range(len(date)):
            item.time.append(date[i] + ' ' + time[i])  #日期+时间
        item.urlhref = html.xpath("//ul/li/a/@href")
        urldetail=[]
        for i in range(len(item.urlhref)):
            item.urlhref[i]='https://help.aliyun.com' + str(item.urlhref[i])
        for j in item.urlhref:
            getContent2 = requests.get(j)
            html2 = etree.HTML(getContent2.text)
            detail = html2.xpath("//div[@class='notice-main-center']//text()")
            resstr = ""
            for text in detail:
                newtext = str(text).strip()
                resstr += newtext + '\n'
            urldetail.append(resstr)
        item.now_totalCount=item.time[0]
        item.urldetail = urldetail
        items.append(item)
        return items

