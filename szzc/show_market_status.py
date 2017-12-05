
from config import *
import restapi

if __name__ == '__main__':
    market = 'ETCCNY'

    print '********************Market********************'
    res = restapi.get_market(market)
    print res, '\n'

    print '********************Depth********************'
    res = restapi.get_depth(market)
    print res, '\n'

    print '********************Ticker********************'
    res = restapi.get_ticker(market)
    print res, '\n'

    print '********************Trades********************'
    res = restapi.get_public_trades(market)
    print res, '\n'