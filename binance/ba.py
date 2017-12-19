# coding=utf-8
import sys
import requests
import json
import os
import time
import subprocess


reload(sys)
sys.setdefaultencoding('utf-8')

timeout = 2

class ba:
    def __init__(self, mykey="", mysecret=""):
        self.mykey    = mykey
        self.mysecret = mysecret

    def getTickers(self):
        url =  'https://api.binance.com/api/v1/ticker/24hr'
        try :
            res = requests.get(url, timeout = timeout)
            tickers = json.loads(res.content)
            # print market + ' ------------->'+ res.content
            if tickers :
                return tickers
        except requests.Timeout as e :
            print e

    

    def outputJs(self, jspath, body):
        with open(jspath,'w') as fo :
            fo.write(body)
            fo.close()


if __name__ == "__main__":
    markets={
            'btc_usdt':'BTCUSDT',
            'bcc_usdt':'BCCUSDT',
            'bcc_btc':'BCCBTC',
            'ltc_usdt':'LTCUSDT',
            'ltc_btc':'LTCBTC',
            'eth_usdt':'ETHUSDT',
            'eth_btc':'ETHBTC',
            'etc_usdt':'ETCUSDT',
            'etc_btc':'ETCBTC',
            'qtum_btc':'QTUMBTC',
            'xrp_usdt':'XRPUSDT',
            'xrp_btc':'XRPBTC',
            'eos_btc':'EOSBTC',
        }

    data={}
    
    nginx_path = '/data/app/nginx/html/'
    # nginx_path = 'd:/'
    tm = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    data = {'up_tm':tm}

    print 'curtm------->',tm
    ba = ba()

    tickers = ba.getTickers()


    for k,v in markets.items() :
        for ele in tickers :
            mkt = v
            if ele['symbol'] == mkt :
                last = ele.get('lastPrice','null')
                data[k] = last

    data['up_tm'] = tm

    temp_file = nginx_path + time.strftime("ba_%Y%m%d%H%M%S.js", time.localtime())
    outStr = "ba_ticker = %s" % json.dumps(data)
    ba.outputJs(temp_file, outStr)

    subprocess.call("cp -rf " + temp_file + " " + nginx_path + "/ba.js", shell=True);
    subprocess.call("rm -rf " + temp_file, shell=True);

        

    