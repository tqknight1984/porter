#!/usr/bin/python
# -*- coding: utf-8 -*- 


import sys
import os
import time

from wxStart import WxStart
from yunUtil import YunUtil
import szzc.szzcUtil as szzcUtil
from threading import Thread


from yunbi.client import Client, get_api_path
from yunbi.conf import ACCESS_KEY, SECRET_KEY

from fileReadUtil import FileReadUtil
from confUtil import ConfUtil


class CreateTrade():
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self, conf_path, pf, coin, price, side, volume, sms_str):
        #sms
        wxStart = WxStart()

        off_tm = ConfUtil(conf_path).getOffByLastTrade(coin)
        print 'off_tm', off_tm
        if off_tm < 5 :
            smsStr =  u'频率限制--> %d' % off_tm
            print smsStr
            wxStart.sendSms('tq', smsStr, "#FFCC00")
            exit(1)
        
        # print u"创建订单咯。。。。"
        # ConfUtil(conf_path).saveLastTrade(coin)

        if u'海' == pf :
            print u'---> hai'
            szzc_or_id = szzcUtil.create_order(coin, side, price, volume)
            # print or_id
            if szzc_or_id > 0 :
                sms_str = u" %s 挂单成功！ %d" % (sms_str, szzc_or_id)
            else :
                sms_str = u" %s 挂单失败！" % (sms_str)

        if u'云' == pf :
            print u'---> yun'
            yun_or_id = YunUtil().createOrder(coin, side, price, volume)
            if yun_or_id > 0 :
                sms_str = u" %s 挂单成功！ %d" % (sms_str, yun_or_id)
            else :
                sms_str = u" %s 挂单失败！" % (sms_str)

        print sms_str

        wxStart.sendSms('tq', sms_str, "#FFCC00")



if __name__ == '__main__':
    arg_len = len(sys.argv)
    # print 'arg_len', arg_len
    if arg_len != 6 :
        print u'参数有误--> 请输入挂单信息， 如：海 zec 2222 sell 1'
        exit(1)
    
    pf = str(sys.argv[1])
    coin = str(sys.argv[2])
    price = float(sys.argv[3])
    side = str(sys.argv[4])
    volume = float(sys.argv[5])

    sms_str = u" >>>  %s %s %s %s %s >>> " % (pf, coin, price, side, volume)
    print sms_str
    
    #频率限制
    conf_path = os.path.split(os.path.realpath(__file__))[0] + "/conf/"

    c = CreateTrade()
    t = Thread(target = c.run, args = (conf_path, pf, coin, price, side, volume, sms_str))
    t.start()
