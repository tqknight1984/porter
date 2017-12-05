
from config import *
import restapi

def testRecordMarket(market=''):
    uri = '/api/rec/market/%s' %market
    print 'GET', uri
    res = restapi.get_market(market)
    print res, '\n'

def testViewDepth(market):
    uri = '/api/rec/depth/%s' %market
    print 'GET', uri
    res = restapi.get_depth(market)
    print res, '\n'

def testViewTicker(market):
    uri = '/api/rec/ticker/%s' %market
    print 'GET', uri
    res = restapi.get_ticker(market)
    print res, '\n'

def testRecordAccount(app_key=trader, sig = signature):
    uri = '/api/rec/account'
    print 'GET', uri
    res =  restapi.get_account(app_key, sig)
    print res, '\n'

def testRecordTrader(app_key=trader, sig = signature):
    uri = '/api/rec/trader'
    print 'GET', uri
    res =  restapi.get_trader(app_key, sig)
    print res, '\n'

def testSessionPosn(mnem='', app_key=trader, sig = signature):
    uri = '/api/sess/posn/%s' % mnem
    print 'GET', uri
    res =  restapi.get_posn(mnem, app_key, sig)
    print res, '\n'

def testSessionOrder(mnem='', id='', app_key=trader, sig = signature):
    uri = '/api/sess/order/'
    if mnem:
        uri += mnem
        if id:
            uri += '/' + id
    print 'GET', uri
    res = restapi.get_order(mnem, id, app_key, sig)
    print res, '\n'

def testSessionTrade(mnem='', id='', app_key=trader, sig = signature):
    uri = '/api/sess/trade/'
    if mnem:
        uri += mnem
        if id:
            uri += '/' + id
    print 'GET', uri
    res = restapi.get_trades(mnem, id, app_key, sig)
    print res, '\n'

def testViewTrades(market):
    uri = '/api/view/trades/' + market
    print uri
    res = restapi.get_public_trades(market)
    print res, '\n'

def testSessionOrder_CreateOrder(market, side, lots, ticks, app_key=trader, sig = signature):
    uri = '/api/sess/order/%s' % market
    print 'POST', uri
    res = restapi.post_order(market,side,lots,ticks,app_key,sig)
    print res, '\n'

def testSessionOrder_CancelOrder(market, ids, app_key=trader, sig = signature):
    uri = '/api/sess/order/'
    if market:
        uri += market
        if ids:
            uri += '/' + ids
    print 'PUT', uri
    res = restapi.put_order(market,ids,0,app_key,sig)
    print res, '\n'

def example(): 
    print restapi.uribase, '\n'

    testRecordMarket()
    testRecordMarket('BTCCNY')
    testViewDepth('BTCCNY')
    testViewTicker('BTCCNY')
    testViewTrades('BTCCNY')
    #"""
    testRecordAccount()
    testRecordTrader()
    print '\n\n'

    testSessionPosn()
    testSessionPosn('ETCCNY')
    print '\n\n'

    testSessionOrder()
    testSessionOrder('BTCCNY')
    testSessionOrder('BTCCNY','3,4')
    print '\n\n'

    testSessionTrade()
    testSessionTrade('BTCCNY')
    testSessionTrade('BTCCNY','5')

    #testSessionOrder_CreateOrder('BTCCNY', 'BUY', 10000, 10000)
    #testSessionOrder_CreateOrder('BTCCNY', 'SELL', 10000, 10000)
    

    testSessionOrder('BTCCNY')
    testSessionTrade('BTCCNY')
    #testSessionOrder_CancelOrder('BTCCNY', '19')
    #"""
if __name__ == '__main__':
    print '\n'
    example()
    print 'Done!'
