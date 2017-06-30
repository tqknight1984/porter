#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import urllib2

from platapi.my_conf import min_operate_num
from platapi.my_conf import min_operate_num

from platapi.lib.client import Client, get_api_path
from platapi.lib.conf import ACCESS_KEY, SECRET_KEY

import sys  

reload(sys)  
sys.setdefaultencoding('utf8')


class YunUtil():

    def __init__(self):
        # self.access_key = access_key
        self.client = Client(access_key=ACCESS_KEY, secret_key=SECRET_KEY)
        # print "yunUtil.init()"

# 获取yun剩余zec
    def getZec(self):
        yun_info = self.client.get(get_api_path('members'))
        # print yun_info

        cny, zec, eth = 0, 0, 0
        accounts = yun_info['accounts']
        for account in accounts:
            if account['currency'] == 'cny':
                cny = account['balance']
            if account['currency'] == 'zec':
                zec = account['balance']
            if account['currency'] == 'eth':
                eth = account['balance']
        return cny, zec, eth

# 获取我的订单信息
    def getMyZecOrder(self):
        markets = self.client.get(get_api_path('markets'))
        print "markets:-->%s" % (markets)
        for market in markets:
            if market['id'] == 'zeccny':
                return self.client.get(get_api_path('orders'), {'market': market['id']})
        return []

# 获取yun有效卖价和数量    asks 卖的数量:remaining_volume 卖的价格:price
    def getSellInfo(self):
        order_book = self.client.get(get_api_path(
            'order_book'), params={'market': 'zeccny'})
        asks = order_book['asks']
        for ask_order in asks:
            remaining_volume = ask_order['remaining_volume']
            price = ask_order['price']
            #  print u"卖出 --> 价格：%s 数量：%s " %(price, remaining_volume)
            if float(remaining_volume) > float(min_operate_num):
                return remaining_volume, price


# 取参数
# path = get_api_path('members')
# signature, query = YunUtil().client.auth.sign_params('GET',path, None)

# print "signature--->%s"  %( signature )
# print "query--->%s"  %( query )


# get member info
print '云币网账户信息： %s(cny), %s(zec), %s(eth)' % (YunUtil().getZec())

print "最少交易量：%f" % (min_operate_num)
remaining_volume, price = YunUtil().getSellInfo()
print '有效卖出价格:%s 有效卖出数量:%s ' % (price, remaining_volume)


# print "btccny--->%s" %(YunUtil().client.get(get_api_path('trades'),
# params={'market': 'zeccny'}))

# while True:
#     off = SosobtcUtil().getOff()
#     time.sleep( 10 )
#     # print "off-------> %s",off
# # zec:yunbi
