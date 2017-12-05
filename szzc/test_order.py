
from config import *
import restapi
import time
import random

if __name__ == '__main__':
    market = 'ETCCNY'

    count = 300
    while count > 0:
        count = count - 1
        side = 'BUY'
        lots = int((100+random.random()*1)*1000)
        ticks = int((3000+random.random()*1)*100)
        res = restapi.post_order(market, side, lots, ticks, trader, signature)
        print res,'\n'

        side = 'SELL'
        lots = int((100+random.random()*1)*1000)
        #ticks = int((3000+random.random()*1)*100)
        res = restapi.post_order(market, side, lots, ticks, trader, signature)
        print res,'\n'
	time.sleep(0.1)

