# -*-coding:utf-8 -*-
# @Time     :   2020/3/16 23:32
# @Author   :   layven
import requests
import re
from lxml import etree

def getcnnvd_count():
    req_url='http://www.cnnvd.org.cn/web/cnnvdnotice/querylist.tag?pageno=1'
    page=(etree.HTML(requests.get(req_url).text)).xpath("//div[@class='page']/a[1]/text()")#获取总条数
    totalcount=int(re.findall(r"\d+", str(page))[0])
    return totalcount

class paramItem(object):
    name=None
    time=None
    urlhref=None
    urldetail = None
    origin = 3#3=CNNVD
    now_totalCount=getcnnvd_count()

class getThreaten_cnnvd(object):
    def __init__(self):
        self.items=self.getContent()

    def getContent(self):
        items = []
        item = paramItem()  # 实例化为对象item
        getContent = requests.get('http://www.cnnvd.org.cn/web/cnnvdnotice/querylist.tag?pageno=1')
        html = etree.HTML(getContent.text)
        item.name = html.xpath("//div[contains(@class,'list_list')]/ul/li/div/a/text()")  # 赋予属性值
        item.time = html.xpath("//div[contains(@class,'fr')]/text()")
        item.urlhref = html.xpath("//div/ul/li/div/a/@href")
        time=[]#作为中间变量
        urldetail=[]
        for i in range(len(item.name)):#存在一堆换行空格，需要处理
            item.name[i] = str(item.name[i]).strip()
        for i in range(len(item.time)):
            item.time[i]=str(item.time[i]).strip()
            if item.time[i]:#去掉换行空格后，需要把空元素处理了
                time.append(item.time[i])
            else:
                pass
        item.time=time
        for i in range(len(item.urlhref)):
            item.urlhref[i]='http://www.cnnvd.org.cn' + str(item.urlhref[i])
        for j in item.urlhref:
            getContent2 = requests.get(j)
            html2 = etree.HTML(getContent2.text)
            detail = html2.xpath("//div[@class='fl w770']//text()")
            resstr = ""
            for text in detail:
                newtext = str(text).split()
                if newtext:
                    newtext = "".join(str(text).split())
                    resstr += newtext.replace(u'\xa0', "").replace(u" ", "") + '\n'
            urldetail.append(resstr)
        item.urldetail=urldetail
        items.append(item)
        return items