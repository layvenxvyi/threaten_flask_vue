#! /usr/bin/python
# -*-coding:utf-8 -*-
# @Time     :   2020-05-27 16:51
# @Author   :   layven


if_exist = 0
shotkey = ''
shottype = ''

#为了找字典里v对应的k，之后优化if-else
def get_key(dict, value):
    return [k for k, v in dict.items() if v == value]

#1操作系统2中间件3开发框架4数据库5web应用6其他
def data_classify(init_if_exist,string):
    global if_exist, shotkey, shottype
    keydic = {1: ['linux', 'window', 'unix', 'mac', 'microsoft', '微软', 'smb'],
              3: ['spring', 'fastjson', 'quartz', 'freemarker', 'jackson', 'velocity', 'zkoss', 'hibernate', 'shiro',
                  'struts2', 'vaadin', 'struts'],
              5: ['ueditor', 'fckeditor', 'kindeditor', 'articlecms', 'videocms', 'ckeditor', 'umeditor', 'xheditor',
                  'thinkphp', 'bootcms', 'codelgniter', 'monstracms', 'wordpress', 'sandbox', 'phpmailer', 'cltphp',
                  'glype', 'discuz!ml', 'xiaoyuancms', 'ygbook', 'discuz!x', 'jenkins', 'wcms', 'zabbix', 'phpmyadmin',
                  'ewebwditor'],
              2: ['tomcat', 'websphere', 'weblogic', 'nginx', 'apache', 'jboss', 'wildfly', 'jetty', 'iis'],
              4: ['memcache', 'hbase', 'mongo', 'mysql', 'mssql', 'postgre', 'redis', 'sqlserver', 'oracle'],
              }#顺序打乱是为了匹配存在多个关键字的时候有个先后顺序，如apache tomcat能匹配到tomcat非apache
    if_exist=init_if_exist#开始取值之前先初始化if_exist
    string_deal = string.replace(' ', '').lower()
    for every_keydic in keydic.values():#遍历5个列表
        if if_exist==1:#已经匹配则不再遍历
            break
        else:
            shottype=''
            shotkey=''
            for key in every_keydic:#遍历5个列表里的每个值
                if key in string_deal:#判断是否包含关键字，包含则为1，打印该关键字，判断关键字所属5种类型
                    if_exist=1#列表里只要满足有包含，则为1，打印该关键字，退出
                    shotkey = key
                    shottype = get_key(keydic, every_keydic)[0]
                    break
                else:
                    shottype=6
    return shotkey,shottype





