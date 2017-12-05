#!/usr/bin/env python

from config import *
import requests
import json

if not uribase:
    uribase = 'https://szzc.com'

def get_market(market=''):
    uri = uribase + '/api/rec/market/%s' % market

    res = requests.get(uri)

    return res.text

def get_trader(trader,sig):
    uri = uribase + '/api/rec/trader'

    res = requests.get(uri,headers = {'app-key':trader,'sig':sig})

    return res.text

def get_account(trader,sig):
    uri = uribase + '/api/rec/account/'

    res = requests.get(uri,headers={'app-key':trader,'sig':sig})

    return res.text

def post_order(market,side,lots,ticks,trader,sig):
    uri = uribase + '/api/sess/order/%s' % market
    postdict = {'side':side,'lots':lots,'ticks':ticks}

    res = requests.post(uri,data=json.dumps(postdict),headers={'app-key':trader,'sig':sig})

    return res.text

def get_order(market,ids,trader,sig):
    uri = uribase + '/api/sess/order/'
    if market:
        uri += market
        if ids:
            uri += '/' + ids

    res = requests.get(uri,headers={'app-key':trader,'sig':sig})
    
    return res.text

def put_order(market,ids,lots,trader,sig):    
    uri = uribase + '/api/sess/order/'
    if market:
        uri += market
        if ids:
            uri += '/' + ids
    jsondict = {'lots':lots}

    res = requests.put(uri,data = json.dumps(jsondict),headers={'app-key':trader,'sig':sig})

    return res.text

def get_trades(market,id,trader,sig):
    uri = uribase + '/api/sess/trade/'
    if market:
        uri += market
        if id:
            uri += '/' + id

    res = requests.get(uri,headers={'app-key':trader,'sig':sig})
    
    return res.text

def get_posn(market,trader,sig):
    uri = uribase + '/api/sess/posn/%s' % market

    res = requests.get(uri,headers={'app-key':trader,'sig':sig})

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




#======tq=======
headers={'apikey':trader,'signature':signature,'Content-Type':'application/json'}


def get_balance(market):
    
    uri = uribase + '/api/trader/balance/%s' % market
    res = requests.get(uri,headers=headers)
    return res.text

def list_balances():
    uri = uribase + '/api/trader/balances'
    # if market:
    #     uri += market
    #     if id:
    #         uri += '/' + id

    resp = requests.get(uri,headers=headers)
    if resp.text :
        return json.loads(resp.text)

def list_active_orders_in_page(market, page):
    uri = uribase + '/api/trader/orderpage/%s/%d' % (market, page)
    res = requests.get(uri,headers=headers)
    
    return res.text

def list_active_orders(market):
    uri = uribase + '/api/trader/orders/%s' % (market)
    res = requests.get(uri,headers=headers)
    return res.text


def create_order(trading_pair, quantity, limit, type, side):
    uri = uribase + '/api/trader/order'
    postdict = {'trading_pair': trading_pair, 'quantity': quantity,
                'limit': limit, 'type': type, 'side': side}
    res = requests.post(uri, data=json.dumps(postdict), headers=headers)
    return res.text

def list_trading_pairs():
    uri = uribase + '/api/trader/trading_pairs'
    res = requests.get(uri,headers=headers)
    return res.text
