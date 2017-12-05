#!/usr/bin/python
# -*- coding: utf-8 -*- 

import ConfigParser
import os
import sys
import pymysql

from confUtil import ConfUtil
# from myConfig import CONF_PATH


# -read(filename)               直接读取文件内容
# -sections()                      得到所有的section，并以列表的形式返回
# -options(section)            得到该section的所有option
# -items(section)                得到该section的所有键值对
# -get(section,option)        得到section中option的值，返回为string类型
# -getint(section,option)    得到section中option的值，返回为int类型，还有相应的getboolean()和getfloat() 函数。


class InitConfig():

    def __init__(self, conf_path):
        print "---> ConfUtil.init()"
        self.conf_path = conf_path


    def getUserConf(self, unames, coins):
        cf = ConfigParser.ConfigParser()
        conf_info = {}
        for uname in unames :
            
            print "--0--->%s" % uname
            print "----->%s" % (self.conf_path + uname + ".config")
            cf.read(self.conf_path + uname + ".config")
            uconf = {}

            #初始化用户配置信息
            for coin in coins :
                coin_info = {}
                if cf.has_section(coin) :
                    notify = cf.get(coin, "notify")
                    logic = cf.get(coin, "logic")
                    offv = cf.get(coin, "offv")

                    coin_info['notify'] = notify
                    coin_info['logic'] = logic
                    coin_info['offv'] = offv
                    uconf[coin] = coin_info

            conf_info[uname] = uconf

        return conf_info


if __name__ == '__main__':
    #都是当前执行pwd目录，不能用
    # conf_path = os.getcwd()
    # os.path.abspath(os.curdir)
    # print os.path.abspath('.') 
    #应该用这个
    conf_path = os.path.split(os.path.realpath(__file__))[0]+"/conf/"
    confutil = ConfUtil(conf_path)

    print conf_path+"==========initconfig=============" + (sys.argv[0])
  # SQL 查询语句
    sql = u"SELECT * FROM obj_logic WHERE uname ='%s' and coin = '%s' " % ("tq", "zec")
    
    if (len(sys.argv) == 1):
        sql = u"SELECT * FROM obj_logic "
    elif (len(sys.argv) == 3):
        sql = u"SELECT * FROM obj_logic WHERE uname ='%s' and coin = '%s' " % (sys.argv[1], sys.argv[2])
    elif (len(sys.argv) == 2):
        sql = u"SELECT * FROM obj_logic WHERE uname ='%s' " % (sys.argv[1])
    else :
        print u'参数有误-->usage: python initConfig.py tq zec'
        exit(1)

    print u"-->sql:%s" % sql

    db_host = "10.105.125.57"
    db_user = "main"
    db_pass = "main"
    db_port = 3306
    db_name = "car_315"
    db = pymysql.connect(host=db_host,user=db_user,passwd=db_pass,db=db_name,port = db_port, use_unicode=1,charset='utf8')
    # print db
    cursor = db.cursor()

    try:
        # 执行SQL语句
        cursor.execute(sql)
        found = cursor.rowcount
        if found :
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                id = row[0]
                openid = row[1]
                uname = row[2]
                coin = row[3]
                max_off = row[4]
                min_off = row[5]
                notify = row[8]
                max_val = row[9]
                min_val = row[10]
                max_ban = row[11]
                min_ban = row[12]
                max_volume = row[13]
                min_volume = row[14]

                # 打印结果
                print ("===========> id=%d,openid=%s,name=%s,coin=%s,max_off=%s,min_off=%s,notify=%s,max_val=%s,min_val=%s" % (id, openid, uname, coin, max_off, min_off, notify, max_val, min_val))
                
                confutil.saveUserLogic(uname, coin, max_off, min_off, notify, max_val, min_val, max_ban, min_ban, max_volume, min_volume)
        else :
            if (len(sys.argv) == 3):
                confutil.delUserLogic(sys.argv[1], sys.argv[2])
                print u"--> del logic !!"
            else:
                print u"--> logic not exists!!"

    except Exception as e:
        print e
        # print ("Error: fetch data or save config exception")

    db.close()

