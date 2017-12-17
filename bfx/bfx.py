#coding=utf-8
import requests  # pip install requests
import json
import base64
import hashlib
import hmac
import time #for nonce
import os
import sys
import subprocess

reload(sys)
sys.setdefaultencoding('utf-8')

class Bfx(object):
    BASE_URL = "https://api.bitfinex.com/"
    KEY=""
    SECRET=""

    def _nonce(self):
        """
        Returns a nonce
        Used in authentication
        """
        return str(int(round(time.time() * 1000)))

    def _headers(self, path, nonce, body):

        signature = "/api/" + path + nonce + body
        # print "Signing: " + signature
        h = hmac.new(self.SECRET, signature, hashlib.sha384)
        signature = h.hexdigest()

        return {
            "bfx-nonce": nonce,
            "bfx-apikey": self.KEY,
            "bfx-signature": signature,
            "content-type": "application/json"
        }

    def api_post(self, path, body={}):
        nonce = self._nonce()
        rawBody = json.dumps(body)
        # print("rawBody-------->"+rawBody)
        headers = self._headers(path, nonce, rawBody)
        # print("url-------->"+self.BASE_URL + path)

        # print("requests.post("+self.BASE_URL + path + ", headers=" + str(headers) + ", data=" + rawBody + ", verify=True)")
        r = requests.post(self.BASE_URL + path, headers=headers, data=rawBody, verify=True)
        if r.status_code == 200:
          return r.json()
        else:
          print r.status_code
          print r
          return ''
        


    def active_orders(self):
        """
        Fetch active orders
        """
        nonce = self._nonce()
        body = {}
        rawBody = json.dumps(body)
        path = "v2/auth/r/orders"


        print(self.BASE_URL + path)
        print(nonce)


        headers = self._headers(path, nonce, rawBody)

        print(headers)
        print(rawBody)


        print("requests.post("+self.BASE_URL + path + ", headers=" + str(headers) + ", data=" + rawBody + ", verify=True)")
        r = requests.post(self.BASE_URL + path, headers=headers, data=rawBody, verify=True)

        if r.status_code == 200:
          return r.json()
        else:
          print r.status_code
          print r
          return ''
    
    def api_get(self, path, params='') :
        url = "https://api.bitfinex.com/v2/%s?%s" % (path, params)
        res = requests.get(url)
        return json.loads(res.text)

    #取当前行情 (买卖价格)
    def get_symb_tick(self, symb):
        path = 'ticker/%s' % symb
        # path = 'tickers'
        res =  self.api_get(path)
        print '------17----->',res
        return (res[0], res[2], res[6])

    #取当前行情
    def get_tick(self, symb):
        path = 'tickers'
        res =  self.api_get(path)
        return res.json
        
    #分别获取买单和卖单的平均价格
    def get_avg_prices(self, symbols):
        body ={
        'start':(time.time() - (10 * 24 * 60 * 60)) * 1000,
        'end':time.time() * 1000,
        'limit':10,
        }
        path = "v2/auth/r/orders/%s/hist" % (symbols)
        res = self.api_post(path = path,body=body)
        # # print 'res--------->',res
        # l = len(res)
        # print 'res--------->',l
        # if l < 1 :
        #     return -1
        amount_buy = 0.0
        amount_sell = 0.0
        price_buy = 0.0
        price_sell = 0.0
        for info in res :
            # print 'info--------->',info
            sbl = info[3]
            order_status = info[13]
            # print 'sbl--------->',sbl
            # print 'order_status--------->',order_status
            # print 'find--------->',order_status.find("CANCELED")
            if order_status.find("CANCELED") != -1 :
                continue
            
            # print 'sbl == symbols--------->',sbl == symbols
            if sbl == symbols :
                amount = float(info[6])
                amount_orig = float(info[7])
                price_avg = float(info[17])
                # print u'买/卖--------->',amount
                # print 'price_avg--------->',price_avg
                if amount != 0.0 :
                    continue
                if price_avg <= 0.0 :
                    continue
                #卖
                if amount_orig < 0.0 :
                    # print u'卖---%s------>%.4f/%.4f' % (coin, amount_orig, price_avg)
                    amount_sell += abs(amount_orig)
                    price_sell += (price_avg * abs(amount_orig))
                
                #买
                if amount_orig > 0.0 and amount == 0.0 :
                    # print u'买---%s------>%.4f/%.4f' % (coin, amount_orig, price_avg)
                    amount_buy += amount_orig
                    price_buy += (price_avg * amount_orig)

        # print 'price_avg_buy--------->',price_avg_buy
        # print 'price_avg_sell--------->',price_avg_sell
        price_avg_buy = price_buy/amount_buy
        price_avg_sell = price_sell/amount_sell
        return (price_avg_buy, price_avg_sell)
     
     #取所有未完结的订单
    def get_act_orders(self):
        active_orders = []
        path = "v2/auth/r/orders"
        res = self.api_post(path = path)
        for info in res :
            symbols = info[3]
            # print 'symbols--------->',symbols
            active_orders.append(symbols)
        return active_orders

    #余额
    def get_account_wallet(self):
        account = {}
        path = "v2/auth/r/wallets"
        res = self.api_post(path = path)
        for info in res :
            way = info[0]
            if way == "exchange" :
                coin = info[1]
                amount = float(info[2])
                account[coin] =  amount
        return account

    #创建订单
    def new_orders(self, symbol, amount, price, side):
        body = {
            'symbol':symbol,
            'amount':amount,
            'price':price,
            'side':side,
            'type':'exchange limit',
            'exchange':'bitfinex',
        }
        path = "v1/order/new"
        res = self.api_post(path = path, body=body)
        print 'res--------->',res

    def outputJs(self, jspath, body):
        with open(jspath,'w') as fo :
            fo.write(body)
            fo.close()

if __name__ == "__main__":
    
    markets={
        'btc_usdt':'BTCUSD',
        'eos_usdt':'EOSUSD',
        'eos_btc':'EOSBTC',
        'eth_usdt':'ETHUSD',
        'eth_btc':'ETHBTC',
        'etc_usdt':'ETCUSD',
        'etc_btc':'ETCBTC',
        'qtum_usdt':'QTMUSD',
        'qtum_btc':'QTMBTC',
        'xrp_usdt':'XRPUSD',
        'xrp_btc':'XRPBTC',
        }

    data={}

    #
    nginx_path = '/data/app/nginx/html/'
    tm = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    

    print 'curtm------->',tm

    bfx = Bfx()

    for k, v in markets.items():
        print k,"------>",v
        symb = 't%s' % v
        #市场的最新买卖价格
        ticker_price = bfx.get_symb_tick(symb)
        print "ticker_price----------->", ticker_price
        data[k] = ticker_price[2]
        print ticker_price

    data['up_tm'] = tm

    temp_file = nginx_path + time.strftime("bfx_%Y%m%d%H%M%S.js", time.localtime())
    outStr = "bfx_ticker = %s" % json.dumps(data)
    bfx.outputJs(temp_file, outStr)


    subprocess.call("cp -rf " + temp_file + " " + nginx_path + "/bfx.js", shell=True);
    subprocess.call("rm -rf " + temp_file , shell=True);


    

    


    
