
from config import *
import restapi

if __name__ == '__main__':
    market = 'ETCCNY'
    side = 'BUY'
    lots = 500*100
    ticks = 10*100 
    res = restapi.post_order(market, side, lots, ticks, trader, signature)
    print res
