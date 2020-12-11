#! /usr/bin/python
# -*-coding:utf-8 -*-
# @Time     :   2020-03-04 18:25
# @Author   :   layven
#写入excel的话需要先运行阿里云和cnnvd的，它怎么调都有编码问题
from xlwt import Workbook
from xlrd import open_workbook
import os
from xlutils.copy import copy

class SaveExcel(object):
    def __init__(self,items):
        self.items=items
        self.run(self.items)
    def run(self,items):#接受调用的参数和接受一个参数
        fileName=u'威胁情报.xls'
        if os.path.exists(fileName):
            oldbook=open_workbook(fileName,formatting_info=True)
            book=copy(oldbook)
            print('open workbook')
        else:
            book=Workbook(encoding='utf8')
        sheet=book.add_sheet(items[0].sheetname,cell_overwrite_ok=True)
        sheet.write(0,0,u'公告时间')
        sheet.write(0,1,u'公告标题')
        sheet.write(0,2,u'公告链接')
        sheet.write(0,3,u'链接详情')
        i=1
        j=1   #目前的表格第几行可以写
        while i <= len(items):#page页数为item有几个,totalCount总共的条目写多少列,pageSize为一页几个，为time里长度
            item=items[i-1]#item里
            k = 1
            while k <=len(item.name):
                sheet.write(j,0,item.time[k-1])#j为位置参数，循环每一页i，写入每个对象的属性的第k个
                sheet.write(j,1,item.name[k-1])
                sheet.write(j,2,item.urlhref[k-1])
                sheet.write(j,3,item.urldetail[k-1])
                j+=1
                k+=1
            i+=1
        book.save(fileName)
if __name__=='__main__':
    pass