#!/usr/bin/python
# -*- coding: utf-8 -*- 

import ConfigParser
import os
import stat
import time


# -read(filename)               直接读取文件内容
# -sections()                      得到所有的section，并以列表的形式返回
# -options(section)            得到该section的所有option
# -items(section)                得到该section的所有键值对
# -get(section,option)        得到section中option的值，返回为string类型
# -getint(section,option)    得到section中option的值，返回为int类型，还有相应的getboolean()和getfloat() 函数。


class ConfUtil():
    def __init__(self, conf_path):
        self.conf_path = conf_path
        # print "ConfUtil.init() --> %s" % conf_path
        if not os.path.exists(conf_path) :
            # print u"创建目录--->%s" % conf_path
            os.makedirs(conf_path)


    def getUserConf(self, unames, coins):
        cf = ConfigParser.ConfigParser()
        conf_info = {}
        for uname in unames :
            
            # print "--0--->%s" % uname
            # print "----->%s" % (self.conf_path + uname + ".config")
            if os.path.isfile(self.conf_path + uname + ".config"):
                cf.read(self.conf_path + uname + ".config")
                uconf = {}

                #初始化用户配置信息
                for coin in coins :
                    if cf.has_section(coin) :
                        coin_info = {}
                        coin_info['notify'] = cf.get(coin, "notify")
                        coin_info['max_off'] = cf.get(coin, "max_off")
                        coin_info['min_off'] = cf.get(coin, "min_off")
                        coin_info['max_val'] = cf.get(coin, "max_val")
                        coin_info['min_val'] = cf.get(coin, "min_val")
                        uconf[coin] = coin_info

                conf_info[uname] = uconf

        return conf_info

    
    def getUserBanConf(self, unames, coins):
        cf = ConfigParser.ConfigParser()
        conf_info = {}
        for uname in unames :
            
            # print "--0--->%s" % uname
            # print "----->%s" % (self.conf_path + uname + ".config")
            if os.path.isfile(self.conf_path + uname + ".config"):
                cf.read(self.conf_path + uname + ".config")
                uconf = {}

                #初始化用户配置信息
                for coin in coins :
                    if cf.has_section(coin) :
                        coin_info = {}
                        coin_info['notify'] = cf.get(coin, "notify")
                        coin_info['max_ban'] = cf.get(coin, "max_ban")
                        coin_info['min_ban'] = cf.get(coin, "min_ban")
                        coin_info['max_volume'] = cf.get(coin, "max_volume")
                        coin_info['min_volume'] = cf.get(coin, "min_volume")
                        uconf[coin] = coin_info

                conf_info[uname] = uconf

        return conf_info

    #是否通知，1|通知 0|否
    def getNotifyCount(self, user):
        cf = ConfigParser.ConfigParser()
        conf_file = self.conf_path + user +".config"
        section = 'notify'
        field_tm = 'last_wave_tm'
        field_count = 'last_wave_count'
        count = 0

        if os.path.exists(conf_file):
            cf.read(conf_file)
            if cf.has_section(section):
                tm = int(cf.get(section, field_tm))
                count = int(cf.get(section, field_count))

                if(int(time.time()-tm) > 7200 ):
                    cf.set(section, field_tm,int(time.time()))
                    cf.set(section, field_count, 0)
                else :
                    cf.set(section, field_count, int(count+1))
            else :
                cf.add_section(section)
                cf.set(section, field_tm,int(time.time()))
                cf.set(section, field_count, 0)

            with open(conf_file,"w+") as f:
                cf.write(f)

        return count
                



    def getOffByLastTrade(self, coin):
        last_tm = 0;
        cf = ConfigParser.ConfigParser()
        conf_file = self.conf_path + "tq.config"
        field = "last_trad_tm"

         # modify cf, be sure to read!
        if os.path.exists(conf_file):
            cf.read(conf_file)
            if cf.has_section(coin) :
                if cf.has_option(coin, field) :
                    last_tm_str = int(cf.get(coin, field))
                    if last_tm_str :
                        last_tm = int(last_tm_str)
            else :
                cf.add_section(coin)
                
            # 写入新的时间戳
            cf.set(coin, field, int(time.time()))
                # write to file
            with open(conf_file,"w+") as f:
                cf.write(f)

        return int(time.time()-last_tm)


#保存最后一次挂单时间
    def saveLastTrade(self, coin):
        cf = ConfigParser.ConfigParser()
        conf_file = self.conf_path + "tq.config"
        field = "last_trad_tm"

         # modify cf, be sure to read!
        if os.path.exists(conf_file):
            cf.read(conf_file)
            if not cf.has_section(coin):
                cf.add_section(coin)
        else :
            cf.add_section(coin)

        cf.set(coin, field, int(time.time()))
         # write to file
        with open(conf_file,"w+") as f:
            cf.write(f)
        print u"write config file success! <<<"


    def saveUserLogic(self, uname, coin, max_off, min_off, notify, max_val, min_val, max_ban, min_ban, max_volume, min_volume):
        print u">>> saveUserLogic()"
        cf = ConfigParser.ConfigParser()
        conf_file = self.conf_path + uname + ".config"

        # modify cf, be sure to read!
        if os.path.exists(conf_file):
            cf.read(conf_file)
            if not cf.has_section(coin):
                cf.add_section(coin)
        else :
            cf.add_section(coin)

        cf.set(coin, "notify",notify)
        cf.set(coin, "max_off",max_off)
        cf.set(coin, "min_off",min_off)
        cf.set(coin, "max_val",max_val)
        cf.set(coin, "min_val",min_val)
        cf.set(coin, "max_ban",max_ban)
        cf.set(coin, "min_ban",min_ban)
        cf.set(coin, "max_volume",max_volume)
        cf.set(coin, "min_volume",min_volume)
        # write to file
        with open(conf_file,"w+") as f:
            cf.write(f)
        print u"write config file success! <<<"

    def delUserLogic(self, uname, coin):
        # print u">>> delUserLogic()"
        cf = ConfigParser.ConfigParser()
        conf_file = self.conf_path + uname + ".config"

        # modify cf, be sure to read!
        if os.path.exists(conf_file):
            cf.read(conf_file)
            if cf.has_section(coin):
                cf.remove_section(coin)
                with open(conf_file,"w+") as f:
                    cf.write(f)
        print u"write config file success! <<<"

if __name__ == '__main__':
    print os.path.abspath('.')
    #test
    # ConfUtil(os.path.abspath('.')+"/").saveUserLogic("zz2", "aaa", "lt", "-5", "1")
    # ConfUtil(os.path.abspath('.')+"/").delUserLogic("zz2","aaa")

    # 
    # print ConfUtil(os.path.abspath('.')+"/conf/").saveLastTrade('zec')
    print ConfUtil(os.path.abspath('.')+"/conf/").getOffByLastTrade('zec')
            






# os.chdir("/Users/app/Documents/zcash/porter/out")

# cf = ConfigParser.ConfigParser()

# # cf.read("test.ini")
# cf.read("/Users/app/Documents/zcash/porter/zzz.config")

# #return all section
# secs = cf.sections()
# print 'sections:', secs, type(secs)
# opts = cf.options("db")
# print 'options:', opts, type(opts)
# kvs = cf.items("db")
# print 'db:', kvs, type(opts)

# #read by type
# db_host = cf.get("db", "db_host")
# db_port = cf.getint("db", "db_port")
# db_user = cf.get("db", "db_user")
# db_pass = cf.get("db", "db_pass")

# #read int
# threads = cf.getint("concurrent", "thread")
# processors = cf.getint("concurrent", "processor")
# print "db_host:", db_host
# print "db_port:", db_port
# print "db_user:", db_user
# print "db_pass:", db_pass
# print "thread:", threads
# print "processor:", processors