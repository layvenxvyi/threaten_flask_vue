# -*-coding:utf-8 -*-
# @Time     :   2020/4/24 23:19
# @Author   :   layven
from flask import Flask, render_template, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import query
from increment.aliThreaten import getThreaten_ali,getTotalCount
from increment.tencentThreaten import getpage,getThreaten_tencent
# from increment.cnnvdThreaten import getcnnvd_count,getThreaten_cnnvd
from increment.nsfocusThreaten import get_now,getThreaten_nsfocus
from type_difinite import data_classify
import json
import requests
import pymysql
pymysql.install_as_MySQLdb()
from flask_cors import CORS

app=Flask(__name__)
cors = CORS(app, resources={r"/.*": {"origins": ["http://127.0.0.1:8080"]}})   # 因为前后端分离一定有跨域问题，所以需要配置只允许特定几个域名跨域

class Config(object):
    #sqlalchemy的配置参数
    SQLALCHEMY_DATABASE_URI="mysql://dbuser:dbpwd@127.0.0.1:3306/dbname"#需要设置为自己的
    #设置sqlalchemy自动跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS=True
app.config.from_object(Config)# 加载配置
db=SQLAlchemy(app)# 创建数据库连接对象

class threaten_test(db.Model):#表选项
    __tablename__='threaten_test'  #设置表名
    id=db.Column(db.Integer,index=True, primary_key=True)#主键不设会报错，对数据库无影响
    origin=db.Column(db.Integer,index=True)
    #origin:阿里云1-腾讯云2-cnnvd3-nsfocus4
    name=db.Column(db.String(64),index=True)
    time=db.Column(db.DateTime(64),index=True)
    urlhref=db.Column(db.String(64),unique=True)
    urldetail=db.Column(db.String(40000),unique=True)
    shotkey=db.Column(db.String(64),index=True)#命中的关键字
    shottype=db.Column(db.Integer,index=True)#命中的类型1操作系统2中间件3开发框架4数据库5web应用6其他

    def __repr__(self):#repr()方法显示一个可读字符串
        pass

class threaten_if_update(db.Model):
    __tablename__='threaten_if_update'
    origin=db.Column(db.Integer(),index=True,primary_key=True)
    totalcount=db.Column(db.String())
    
@app.route('/')
def index():
    return {'hello':'threaten!'}

@app.route('/query_threaten',methods=['GET', 'POST'])
def getdata():
    arr1={'1':'阿里云','2':'腾讯云','3':'CNNVD','4':'绿盟'}
    arr2={'1':'操作系统','2':'中间件','3':'开发框架','4':'数据库','5':'web应用','6':'其他'}
    arr3 = {'操作系统': ['linux', 'window', 'unix', 'mac', 'microsoft', '微软', 'smb'],
            '中间件': ['tomcat', 'websphere', 'weblogic', 'nginx', 'apache', 'jboss', 'wildfly', 'jetty', 'iis'],
            'web框架': ['spring', 'fastjson', 'quartz', 'freemarker', 'jackson', 'velocity', 'zkoss', 'hibernate', 'shiro',
                  'struts2', 'vaadin', 'struts'],
            'web应用': ['memcache', 'hbase', 'mongo', 'mysql', 'mssql', 'postgre', 'redis', 'sqlserver', 'oracle'],
            '数据库': ['ueditor', 'fckeditor', 'kindeditor', 'articlecms', 'videocms', 'ckeditor', 'umeditor', 'xheditor',
                  'thinkphp', 'bootcms', 'codelgniter', 'monstracms', 'wordpress', 'sandbox', 'phpmailer', 'cltphp',
                  'glype', 'discuz!ml', 'xiaoyuancms', 'ygbook', 'discuz!x', 'jenkins', 'wcms', 'zabbix', 'phpmyadmin',
                  'ewebwditor'],
              }
    select_type=request.form.get("select_type", '0')
    select_origin=request.form.get("select_origin", '0')
    select_shotkey=request.form.get("select_shotkey",[])
    if select_shotkey==[''] or select_shotkey=='':
        select_shotkey=[]
    else:
        select_shotkey=select_shotkey.split(',')
    select_val={"select_type":select_type,"select_origin":select_origin,"select_shotkey":select_shotkey}
    pageid = request.form.get('page', 1, type=int)
    print(select_val)
    returnObj = {}
    if select_val=={'select_type': '0', 'select_origin': '0', 'select_shotkey': []}:
        event2 = threaten_test.query.order_by(threaten_test.time.desc()).order_by(threaten_test.id.desc()).paginate(pageid)  # 先orderby再limit
        returnList=eventdata_json(event2,arr1,arr2)
        returnObj['total'] = event2.total
        returnObj['data'] = returnList
    else:
        event2=return_data(select_val,pageid)
        returnObj['total'] = event2.total
        returnObj['data'] = eventdata_json(event2,arr1,arr2)
    returnObj['orgin_Options'] = arr1
    returnObj['type_Options'] = arr2
    returnObj['shotkey_Options'] = arr3
    return json.dumps(returnObj)

def eventdata_json(event2,arr1,arr2):
    #对初始数据做处理，返回前端json数据
    returnList = []
    for item in event2.items:
        del item.__dict__['_sa_instance_state']
        item.__dict__['time'] = datetime.strftime(item.__dict__['time'], '%Y-%m-%d %H:%M:%S')
        returnList.append(item.__dict__)
    for item in returnList:
        #替换为文字
        item['origin'] = arr1[str(item['origin'])]
        item['shottype'] = arr2[str(item['shottype'])]
    return returnList

def return_data(select_val,pageid):#单独函数处理筛选的数据
    type=select_val['select_type']
    origin=select_val['select_origin']
    shotkey=select_val['select_shotkey']
    event=threaten_test.query.order_by(threaten_test.time.desc())
    if shotkey:
        if type == '0' and origin == '0':
            event2 = event.filter(threaten_test.shotkey.in_(shotkey)).paginate(pageid)
        elif origin.isdigit() and type == '0':
            event2 = event.filter(threaten_test.origin == origin,threaten_test.shotkey.in_(shotkey)).paginate(pageid)
        elif type.isdigit() and origin == '0':
            event2 = event.filter(threaten_test.shottype == type,threaten_test.shotkey.in_(shotkey)).paginate(pageid)
        elif type.isdigit() and origin.isdigit():
            event2 = event.filter(threaten_test.origin == origin,threaten_test.shottype == type,threaten_test.shotkey.in_(shotkey)).paginate(pageid)
    else:
        if origin.isdigit() and type == '0':
            event2 = event.filter_by(origin=origin).paginate(pageid)
        elif type.isdigit() and origin == '0':
            event2 = event.filter_by(shottype=type).paginate(pageid)
        elif type.isdigit() and origin.isdigit():
            event2 = event.filter_by(origin=origin, shottype=type).paginate(pageid)
    return event2


class updata_Threaten(object):#更新爬取数据的类
    def __init__(self):
        # self.ali_if_update()
        # self.tencent_if_update()
        # self.cnnvd_if_update()
        self.nsfocus_if_update()
        self.data_deal()

    def update_data(self,items,count):#相当于之前脚本的savetoexcel的效果，现在对对象执行sql操作
        i = 1#items为对象，count参数为取对象的几个值，在数据库里就是几条数据
        while i <= len(items):
            item = items[i - 1]
            k = 1
            while k <=count:
                itemdata=threaten_test(origin=items[0].origin,name=item.name[k-1],time=item.time[k-1],urlhref=item.urlhref[k-1],urldetail=item.urldetail[k-1])
                db.session.add(itemdata)
                k+=1
            i+=1
        #更新判断是否爬取的数据表
        threaten_if_update.query.filter_by(origin=items[0].origin).update({'totalcount':items[0].now_totalCount})
        db.session.commit()

    def ali_if_update(self):
        new_totalCount=getTotalCount()#取时间值的列表，非上次爬取的总条数，因为阿里云默认返回200条数，不再增加
        old_totalCount=threaten_if_update.query.filter_by(origin='1').first()
        ali_updataCount=0
        if old_totalCount.totalcount in new_totalCount:
            ali_updataCount=new_totalCount.index(old_totalCount.totalcount)
        item=getThreaten_ali().items
        if ali_updataCount>0:
            self.update_data(item,ali_updataCount)
        else:
            print('阿里云没有更新')
            
    def tencent_if_update(self):
        new_totalCount=getpage()
        old_totalCount=threaten_if_update.query.filter_by(origin='2').first()
        if new_totalCount>int(old_totalCount.totalcount):
            tencent_updateCount=new_totalCount-int(old_totalCount.totalcount)
            item=getThreaten_tencent().items
            self.update_data(item,tencent_updateCount)
        else:
            print('腾讯云没有更新')

    # def cnnvd_if_update(self):
    #     new_totalCount=getcnnvd_count()
    #     old_totalCount=threaten_if_update.query.filter_by(origin='3').first()
    #     if new_totalCount>old_totalCount.totalcount:
    #         cnnvd_updateCount=new_totalCount-old_totalCount.totalcount
    #         item=getThreaten_cnnvd().items
    #         self.update_data(item,cnnvd_updateCount)
    #     else:
    #         print('cnnvd没有更新')

    def nsfocus_if_update(self):
        new_totalCount = get_now()#取article的id值的列表，非上次爬取的总条数，nsfocus因为只取3页，所以判断较其他三个特殊处理
        old_totalCount = threaten_if_update.query.filter_by(origin='4').first()
        nsfocus_updateCount=0
        for i in new_totalCount:
            if i>int(old_totalCount.totalcount):
                nsfocus_updateCount+=1
        item = getThreaten_nsfocus().items
        # nsfocus_updateCount-=(8-len(item[0].name))
        if nsfocus_updateCount>0:
            self.update_data(item,nsfocus_updateCount)
        else:
            print('绿盟没有更新')
            
    def data_deal(self):#结果一份推送，一份写入数据库
        orgin_name = threaten_test.query.filter_by(shottype=None).all()
        for i in orgin_name:
            shotkey,shottype=data_classify(0,i.name)#开始取值之前先初始化if_exist=0赋值过去
            #触发推送
            self.wx_Sendmessage(i,shotkey,shottype)
            #写入数据库
            threaten_test.query.filter_by(name=i.name).update({'shotkey': shotkey,'shottype':shottype})
        db.session.commit()


    def wx_Sendmessage(self,content,shotkey,shottype):#调用微信接口进行消息推送http://wxpusher.zjiecode.com/admin/app/list
        if shottype==1:
            type='操作系统'
        elif shottype==2:
            type='中间件'
        elif shottype==3:
            type='开发框架'
        elif shottype==4:
            type='数据库'
        elif shottype==5:
            type='web应用'
        else:
            type='其他'
        content_data = "<a href='http://192.168.43.218:8080/query_threaten'>点击查看以往威胁情报</a >" + \
                        '\n\n' + content.name + '\n' + str(content.time) + '\n' + '原始链接：' + content.urlhref + '\n' + \
                        '命中类型/关键字：' + type + '/' + shotkey + '\n' + '漏洞详情：' + content.urldetail
        # //内容类型 1表示文字 2表示html(只发送body标签内部的数据即可，不包括body标签) 3表示markdown
        url = 'http://wxpusher.zjiecode.com/api/send/message'
        #使用自己的token及主题id
        params = {"appToken": "此处请填入自己注册的appToken",
                  "content": content_data, "contentType": 1, "topicIds": [428], "uids": [], "url": "http://192.168.43.218:8080/query_threaten"}
        params = json.dumps(params)
        headers = {'Content-Type': 'application/json', }
        html = requests.post(url, data=params, headers=headers)
        print(html.text)

from apscheduler.schedulers.background import BackgroundScheduler
def scheduler_func():
    scheduler = BackgroundScheduler()  # 非阻塞 A scheduler that runs in the background using a separate thread
    try:
        #测试
        scheduler.add_job(func=updata_Threaten, trigger='cron', second='*/10', id='start_update')
        #生产
        #scheduler.add_job(func=updata_Threaten, trigger='cron', hour='*/2', id='start_update')
        scheduler.start()
    except:
        params = {"appToken": "此处请填入自己注册的appToken","content": '脚本运行出错了', "contentType": 1, "topicIds": [428], "uids": [], "url": ""}
        html = requests.post('http://wxpusher.zjiecode.com/api/send/message', data=params, headers={'Content-Type': 'application/json', })
        print(html)

if __name__=='__main__':
    scheduler_func()
    app.run(host='0.0.0.0',port=8888,debug=True,use_reloader=False)#debug模式默认会对程序再执行一次，所以后面要加use_reloader=Flase，不写端口则默认5000


