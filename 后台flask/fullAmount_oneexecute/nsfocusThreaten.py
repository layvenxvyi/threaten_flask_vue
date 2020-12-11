# -*-coding:utf-8 -*-
# @Time     :   2020/3/16 21:41
# @Author   :   layven
import requests
from saveToExcel import SaveExcel
from lxml import etree
import re

class paramItem(object):
    name=None
    time=None
    urlhref=None
    urldetail = None
    sheetname = u'绿盟'
class getThreaten_nsfocus(object):
    def __init__(self):
        self.urls = ['http://blog.nsfocus.net/category/threat-alert/']
        self.geturl()
        self.items=self.getContent()
        SaveExcel(self.items)
    def geturl(self):
        base_url='http://blog.nsfocus.net/category/threat-alert/page/'
        for n in range(2,6):#爬2,3,4,5页面即可，加上列表有的第一页
            url=base_url+str(n)+'/'
            self.urls.append(url)
    def getContent(self):
        items = []
        for url in self.urls:
            item=paramItem()#实例化为对象item
            getContent = requests.get(url)
            html = etree.HTML(getContent.text)
            name = html.xpath("//h2/a/text()")  # 赋予属性值
            time = html.xpath("//div/span/a/time/span/text()")#取日期和时间则@datetime
            urlhref = html.xpath("//h2/a/@href")
            item.name=[]
            item.time=[]
            item.urlhref=[]
            urldetail = []
            for i in range(len(name)):#去除页面可能存在的绿盟威胁周报的内容
                if u'绿盟' not in name[i]:
                    item.name.append(name[i])
                    item.time.append(time[i])
                    item.urlhref.append(urlhref[i])
                else:
                    pass
            for j in item.urlhref:
                getContent2 = (requests.get(j).text).replace('\n', '')
                html_res = re.sub(r"<table.*?</table>", "", getContent2)  # 去除代码框中的所有重复语句，非贪婪模式
                html2 = etree.HTML(html_res)
                detail = html2.xpath('//p//text()')  # 只取文本，图片太难了，遂弃之
                resstr = ""  # 处理取到的文本
                for text in detail:
                    resstr += text + '\n'
                urldetail.append(resstr)
            item.urldetail=urldetail
            items.append(item)
        return items

if __name__=='__main__':
    getThreaten_nsfocus()