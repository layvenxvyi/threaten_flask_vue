# -*-coding:utf-8 -*-
# @Time     :   2020/3/16 21:41
# @Author   :   layven
import requests
from lxml import etree
import re

def get_now():
    getContent = requests.get('http://blog.nsfocus.net/category/threat-alert/page/1')
    html = etree.HTML(getContent.text)
    now_postid = html.xpath("//article/@id")
    totalcount=[]
    for postid in now_postid:
        count = int(re.findall(r"\d+",str(postid))[0])
        totalcount.append(count)
    return totalcount

class paramItem(object):
    name=None
    time=None
    urlhref=None
    urldetail = None
    origin = 4#4=绿盟
    now_totalCount=None

class getThreaten_nsfocus(object):
    def __init__(self):
        self.items=self.getContent()

    def getContent(self):
        items = []
        item=paramItem()#实例化为对象item
        getContent = requests.get('http://blog.nsfocus.net/category/threat-alert/page/1')
        html = etree.HTML(getContent.text)
        name = html.xpath("//h2/a/text()")  # 赋予属性值
        time = html.xpath("//div/span/a/time/span/text()")  # 取日期和时间则@datetime
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
        postid = html.xpath("//article/@id")[0]
        item.now_totalCount=int(re.findall(r"\d+", str(postid))[0])
        item.urldetail=urldetail
        items.append(item)
        return items
