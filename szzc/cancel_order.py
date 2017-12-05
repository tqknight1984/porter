
from config import *
import restapi

if __name__ == '__main__':
    market = 'ETCCNY'
    lots = 0
    ids = '76029,76028'
    res = restapi.put_order(market, ids, lots, trader, signature)
    print res