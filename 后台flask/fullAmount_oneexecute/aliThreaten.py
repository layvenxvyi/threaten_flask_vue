#! /usr/bin/python
# -*-coding:utf-8 -*-
# @Time     :   2020-03-04 18:24
# @Author   :   layven
import requests
from saveToExcel import SaveExcel
from lxml import etree

class paramItem(object):
    name=None
    time=None
    urlhref=None
    urldetail=None
    sheetname=u'阿里云'

class getThreaten_ali(object):
    def __init__(self):
        self.urls=[]
        self.getpage()
        self.geturl()
        self.items=self.getContent()
        SaveExcel(self.items)

    def getpage(self):
        getContent = requests.get('https://help.aliyun.com/notice_list_page/9213612/1.html')
        html = etree.HTML(getContent.text)
        page = html.xpath("//script[last()]/text()")
        string1 = str(page[0])#转换类型string
        list1= string1.split(":")#取值处理
        totalCount = int(list1[1].split(",")[0])#获取总条数
        pageSize= int(list1[3].split(",")[0])#获取每一页展示数
        page = int(totalCount/pageSize)+1#计算得到总页数
        return page

        # print totalCount
        # print pageSize

    def geturl(self):
        for n in range(1,self.getpage()+1):#获取所有要请求的url
            url='https://help.aliyun.com/notice_list_page/9213612/'+str(n)+'.html'
            self.urls.append(url)

    def getContent(self):
        items=[]
        for url in self.urls:
            item=paramItem()#实例化为对象item
            getContent = requests.get(url)
            # print getContent.text
            html = etree.HTML(getContent.text)
            item.name = html.xpath("//ul/li/a/text()")#赋予属性值
            item.time = html.xpath("//ul/li/span/text()")
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
            item.urldetail = urldetail
                # path_wk = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'  # 安装位置
                # config = pdfkit.configuration(wkhtmltopdf=path_wk)
                # pdfkit.from_url(urlhref[i],str(i+1+u*count)+'_'+str(time[i])+'.pdf', configuration=config)
            items.append(item)
        # print items[0]<__main__.paramItem object at 0x10a3a1e50>,items[0].name[0]里面有一页里的所有名字
        # print items[1].time
        return items
if __name__=='__main__':
    getThreaten_ali()
