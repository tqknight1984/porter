#!/usr/bin/python
# -*- coding: utf-8 -*- 


import sys

from wxStart import WxStart
from yunUtil import YunUtil
from szzc import szzcUtil

from yunbi.client import Client, get_api_path
from yunbi.conf import ACCESS_KEY, SECRET_KEY

class ClearOrder():
    def __init__(self):
        print "---> ClearOrder.init()"


if __name__ == '__main__':
    wxStart = WxStart()
    yunbi = YunUtil()

    msgStr = '没有可取消的订单'
    #yunbi
    res = yunbi.clearOrder()
    if len(res) > 0 :
        msgStr = '已取消订单：'
        for order in res :
            msgStr += '云%s%s%s%s；' % (order['market'], order['price'], order['side'], order['volume'])
    # print msgStr
    
    wxStart.sendSms('tq', msgStr, "#990000")
    


