# coding=utf-8
import sys
import requests
import json
import os
import time
import subprocess


reload(sys)
sys.setdefaultencoding('utf-8')

timeout = 1

class bfx2zb:
    def __init__(self, mykey="", mysecret=""):
        self.mykey    = mykey
        self.mysecret = mysecret

    def getZbTicker(self, market):
        url =  'http://api.zb.com/data/v1/ticker?market=%s' % market
        try :
            res = requests.get(url, timeout = timeout)
            jo = json.loads(res.content)
            print market + ' ------------->'+ res.content
            ticker = jo.get("ticker",None)
            if ticker :
                return ticker.get('last', "null")
        except requests.Timeout as e :
            print e


    def outputJs(self, jspath, body):
        with open(jspath,'w') as fo :
            fo.write(body)
            fo.close()


if __name__ == "__main__":

    markets={
        'btc_usdt':'btc_usdt',
        'eos_usdt':'eos_usdt',
        'eos_btc':'eos_btc',
        'eth_usdt':'eth_usdt',
        'eth_btc':'eth_btc',
        'etc_usdt':'etc_usdt',
        'etc_btc':'etc_btc',
        'qtum_usdt':'qtum_usdt',
        'qtum_btc':'qtum_btc',
        'xrp_usdt':'xrp_usdt',
        'xrp_btc':'xrp_btc',
        }

    data={}
    
    nginx_path = '/data/app/nginx/html/'
    tm = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    data = {'up_tm':tm}

    print 'curtm------->',tm
    bz = bfx2zb()

    for k,v in markets.items() :
        mkt = v
        last = bz.getZbTicker(mkt)
        data[mkt] = last
        print last

    data['up_tm'] = tm

    temp_file = nginx_path + time.strftime("zb_%Y%m%d%H%M%S.js", time.localtime())
    outStr = "zb_ticker = %s" % json.dumps(data)
    bz.outputJs(temp_file, outStr)

    subprocess.call("cp -rf " + temp_file + " " + nginx_path + "/zb.js", shell=True);
    subprocess.call("rm -rf " + temp_file , shell=True);


        

    
    # res = requests.get(url)
    # jo = json.loads(res.content)
    # print jo
    # ticker = jo.get('ticker',None)
    # print (ticker)