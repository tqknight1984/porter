#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import urllib2

import utils.gmtTimeUtil as gmtTimeUtil

from yunbi.client import Client, get_api_path
from yunbi.conf import ACCESS_KEY, SECRET_KEY

import sys  

reload(sys)  
sys.setdefaultencoding('utf8')


class YunUtil():

    def __init__(self):
        # self.access_key = access_key
        self.client = Client(access_key=ACCESS_KEY, secret_key=SECRET_KEY)
        # print "yunUtil.init()"


    def getMebersInfo(self):
        try:
            yun_info = self.client.get(get_api_path('members'))
            return yun_info
        except Exception, e:
            print e
        return None

# 获取yun剩余zec
    def getCurrency(self, coin):
        yun_info = self.client.get(get_api_path('members'))
        # print yun_info

        # cny, zec, eth = 0, 0, 0
        balance = 0.0
        accounts = yun_info['accounts']
        for account in accounts:
            if account['currency'] == coin:
                balance = float(account['balance'])
        return balance

# 获取我的挂单数
    def getMyOrderCount(self, coin):
        orders = self.client.get(get_api_path('orders'), {'market': coin+'cny'})
        # print orders
        count = 0
        off_sec = 0
        for order in orders :
            if order['state'] == 'wait' :
                count = count + 1
                created_at = order['created_at']
                # print "gmt_tm--->"+created_at
                off_sec = gmtTimeUtil.get_off_by_utc_str(created_at)
                # print "off_sec--->%d" % off_sec
                # 如果超过 10分钟，提醒手动处理
                if off_sec > 600 :
                    return 600
        return count

# 获取yun有效卖价和数量    asks 卖的数量:remaining_volume 卖的价格:price    bids 买
    def getMarketInfo(self, buyOrSell, coin, max_volume, min_volume):
        order_book = self.client.get(get_api_path('order_book'), params={'market': coin+'cny'})
        # print order_book
        side = ''
        if 'buy' == buyOrSell :
            side = 'bids'
        if 'sell' == buyOrSell :
            side = 'asks'
        asks = order_book[side]
        for ask_order in asks:
            remaining_volume = float(ask_order['remaining_volume'])
            price = float(ask_order['price'])
            #  print u"卖出 --> 价格：%s 数量：%s " %(price, remaining_volume)
            #交易量限制
            if remaining_volume >= min_volume:
                if remaining_volume > max_volume :
                    remaining_volume = max_volume
                return remaining_volume, price

        return 0.0, 0.0

    
    #创建订单
#sell 10 dogecoins at price 0.01
# params = {'market': 'dogcny', 'side': 'sell', 'volume': 10, 'price': 0.01}
# res = client.post(get_api_path('orders'), params)
    def createOrder(self, coin, buyOrSell, price, volume):
        # print coin, buyOrSell, price, volume
        try :
            params = {'market': coin+'cny', 'side': buyOrSell, 'volume': volume, 'price': price}
            res = self.client.post(get_api_path('orders'), params)
            # print 'res', res
            if res and res['id'] > 1 :
                return res['id']
        except Exception, e :
            print e
            
        return 0


#取消所有订单
    def clearOrder(self):
        res = self.client.post(get_api_path('clear'))
        # print res
        return res

if __name__ == '__main__':
    
    print u"---", "====="

    # 取参数
    # path = get_api_path('members')
    # signature, query = YunUtil().client.auth.sign_params('GET',path, None)

    # print "signature--->%s"  %( signature )
    # print "query--->%s"  %( query )


    # get member info
    # print u'云币网账户信息： %d(cny)' % (YunUtil().getCurrency('cny'))

    # print "最少交易量：%f" % (min_operate_num)
    # remaining_volume, price = YunUtil().getMarketInfo('sell', 'eth', 20, 1)
    # print '有效价格:%f 有效数量:%f ' % (price, remaining_volume)

    # print u'云币网账户信息： %s(cny)' % (YunUtil().getMyOrderCount('zec'))
    # print time.strftime("%Y-%m-%d %H:%M:%S", time.time()) 
    # print u'创建订单： %s' % (YunUtil().createOrder('zec', 'buy', 100, 1.00))
    # print u'创建订单： %s' % (YunUtil().createOrder('eos', 'sell', 14, 1.00))
    YunUtil().clearOrder()
