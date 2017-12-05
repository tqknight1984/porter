
from config import *
import restapi
import json

def main():
    market = 'BTCCNY'
    lots = 0
    idlist= []

    print '\n********************Cancel All Orders********************\n'
    res = restapi.get_order(market, '', trader, signature)
    orders = json.loads(res)
    if not orders:
        print 'Not Order Found!\n'
        return

    for order in orders:
       idlist.append(str(order['id']))

    pos = 0
    step = 100
    while True:
        ids = ','.join(idlist[pos : pos+step])
        pos = pos + step
        if len(ids) > 0:
            res = restapi.put_order(market, ids, lots, trader, signature)
            print res
            print len(ids), 'orders processed.\n'
        else:
            break

if __name__ == '__main__':
    main()
