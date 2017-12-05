
from config import *
import restapi
import json

if __name__ == '__main__':
    market = 'ETCCNY'
    orderids = ''
    tradeid = ''
    txtlimit = 4096
    
    print '********************Account********************'
    res =  restapi.get_account(trader, signature)
    print res, '\n'

    print '********************Trader********************'
    res =  restapi.get_trader(trader, signature)
    print res, '\n'

    print '********************Position********************'
    res =  restapi.get_posn(market, trader, signature)
    print res, '\n'

    print '********************Order********************'
    res = restapi.get_order(market, orderids, trader, signature)
    print 'TRUNC...['+str(len(json.loads(res))) + '] ' + res[-txtlimit:-1] if len(res)>txtlimit else res, '\n'

    print '********************Trades********************'
    res = restapi.get_trades(market, tradeid, trader, signature)
    #print 'TRUNC... ' + res[-txtlimit:-1] if len(res)>txtlimit else res, '\n'
    print 'TRUNC...['+str(len(json.loads(res))) + '] ' + res[-txtlimit:-1] if len(res)>txtlimit else res, '\n'

