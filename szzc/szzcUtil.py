#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import datetime
from config import *
import requests
import json




if not uribase:
    uribase = 'https://szzc.com'

headers = {'apikey': trader, 'signature': signature,
           'Content-Type': 'application/json'}

SZZC_KK = 100000000

# class SzzcUtil():


def __init__(self):
    print "SzzcUtil.init()"


def get_market(market=''):
    uri = uribase + '/api/rec/market/%s' % market

    res = requests.get(uri)

    return res.text


def get_trader(trader, sig):
    uri = uribase + '/api/rec/trader'

    res = requests.get(uri, headers={'app-key': trader, 'sig': sig})

    return res.text


def get_account(trader, sig):
    uri = uribase + '/api/rec/account/'

    res = requests.get(uri, headers={'app-key': trader, 'sig': sig})

    return res.text


def post_order(market, side, lots, ticks, trader, sig):
    uri = uribase + '/api/sess/order/%s' % market
    postdict = {'side': side, 'lots': lots, 'ticks': ticks}

    res = requests.post(uri, data=json.dumps(postdict),
                        headers={'app-key': trader, 'sig': sig})

    return res.text


def get_order(market, ids, trader, sig):
    uri = uribase + '/api/sess/order/'
    if market:
        uri += market
        if ids:
            uri += '/' + ids

    res = requests.get(uri, headers={'app-key': trader, 'sig': sig})

    return res.text


def put_order(market, ids, lots, trader, sig):
    uri = uribase + '/api/sess/order/'
    if market:
        uri += market
        if ids:
            uri += '/' + ids
    jsondict = {'lots': lots}

    res = requests.put(uri, data=json.dumps(jsondict),
                       headers={'app-key': trader, 'sig': sig})

    return res.text


def get_trades(market, id, trader, sig):
    uri = uribase + '/api/sess/trade/'
    if market:
        uri += market
        if id:
            uri += '/' + id

    res = requests.get(uri, headers={'app-key': trader, 'sig': sig})

    return res.text


def get_posn(market, trader, sig):
    uri = uribase + '/api/sess/posn/%s' % market

    res = requests.get(uri, headers={'app-key': trader, 'sig': sig})

    return res.text


def get_public_trades(market):
    uri = uribase + '/api/view/trades/%s' % market

    res = requests.get(uri)

    return res.text


def get_depth(market):
    uri = uribase + '/api/view/depth/%s' % market

    res = requests.get(uri)

    return res.text


def get_ticker(market):
    uri = uribase + '/api/view/ticker/%s' % market

    res = requests.get(uri)

    return res.text


#==================tq=======================

# 获取市场有效买卖价格，数量
def getMarketInfo(buyOrSell, coin , max_volume, min_volume):
    market = coin.upper() + 'CNY'
    uri = uribase + '/api/public/depth/%s' % market
    resp = requests.get(uri)
    if resp.text:
        order_book = json.loads(resp.text)
        #print order_book

        if order_book['status']['success'] == 1:
            side = ''
            if 'buy' == buyOrSell:
                side = 'bid'
            if 'sell' == buyOrSell:
                side = 'ask'
            asks = order_book['result'][side]
            for ask_order in asks:
                price = float(ask_order[0]) / SZZC_KK
                remaining_volume = float(ask_order[1]) / SZZC_KK
                #交易量限制
                if remaining_volume >= min_volume:
                    if remaining_volume > max_volume :
                        remaining_volume = max_volume
                    return remaining_volume, price

    return 0.0, 0.0


# 获取账户中数字币数量
def get_balance(coin):
    market = coin.upper()
    uri = uribase + '/api/trader/balance/%s' % market
    resp = requests.get(uri, headers=headers)
    if resp.text:
        res_info = json.loads(resp.text)
        #print res_info

    if res_info['status']['success'] == 1 and market == res_info['result']['symbol']:
        balance = res_info['result']['balance']
        return float(balance) / SZZC_KK

    return 0.0


# 抓取账户信息
def list_balances():
    try:
        uri = uribase + '/api/trader/balances'
        # if market:
        #     uri += market
        #     if id:
        #         uri += '/' + id

        resp = requests.get(uri, headers=headers)
        if resp.text:
            return json.loads(resp.text)
    except Exception, e :
        print e
    
    return None


def list_active_orders_in_page(market, page):
    uri = uribase + '/api/trader/orderpage/%s/%d' % (market, page)
    res = requests.get(uri, headers=headers)

    return res.text

#取当前我的挂单数
def getMyOrderCount(coin):
    market = coin.upper()+'CNY'
    uri = uribase + '/api/trader/orders/%s' % (market)
    resp = requests.get(uri, headers=headers)
    count = 0
    if resp.text:
        res_info = json.loads(resp.text)
        # print res_info
        if res_info['status']['success'] == 1 :
            result = res_info['result']
            for order in result :
                count = count +1
                #操过 XX秒 未成交，提醒
                created = order['created']
                created_tm = datetime.datetime.fromtimestamp(created/1000)
                now_tm = datetime.datetime.fromtimestamp(time.time())
                off_sec = (now_tm - created_tm).seconds
                # print off_sec
                # 如果超过 10分钟，提醒手动处理
                if off_sec > 600 :
                    return 600
    return count


#创建订单
def create_order(coin, buyOrSell, price, volume):
    # print coin, '-----', buyOrSell, '-----', price, '-----', volume
    try :
        uri = uribase + '/api/trader/order'
        trading_pair = coin.upper() + 'CNY'
        side = buyOrSell.upper()
        limit = price * SZZC_KK
        #重复5次，创建订单经常失败
        for i in range(1, 5) :
            quantity  = volume * SZZC_KK
            postdict = {'trading_pair': trading_pair, 'quantity': quantity,
                    'limit': limit, 'type': 'LIMIT', 'side': side}
            resp = requests.post(uri, data=json.dumps(postdict), headers=headers)
            if resp.text:
                res_obj = json.loads(resp.text)
                if res_obj['status']['success'] == 1 :
                    return res_obj['result']['order_id']
                else :
                    volume = max(0.01, volume - 0.01)
                    print u"szzc 创建订单第", i, u"次失败！next volume: ", volume, res_obj
            
    except Exception, e :
        print e
    return 0

#取消订单 这个方法海枫藤失效了
def cancel_order(coin, order_id):
    market = coin.upper() + 'CNY'
    uri = uribase + '/api/trader/orders/%s/%s' % (market, order_id)
    resp = requests.get(uri, headers=headers)
    if resp.text:
        res_obj = json.loads(resp.text)
        return res_obj
        # if res_obj['status']['success'] == 1 :
        #     return res_obj['result']['order_id']
    return 0


def list_trading_pairs(self):
    uri = uribase + '/api/trader/trading_pairs'
    res = requests.get(uri, headers=headers)
    return res.text


if __name__ == '__main__':
    print "---"
    # print getMarketInfo('sell', 'etc')
    # print get_balance('cny')
    # print getMyOrderCount('eth')

    print create_order('zec', 'sell', 1800.51, 2.40);

    # 73444239
    # print cancel_order('zec', 73444239);