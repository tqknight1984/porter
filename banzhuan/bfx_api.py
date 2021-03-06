#coding=utf-8
import requests  # pip install requests
import json
import base64
import hashlib
import hmac
import time #for nonce
import os
import sys, getopt
import subprocess

from banDao import banDao
import conf


reload(sys)
sys.setdefaultencoding('utf-8')

class bfx_api(object):
    BASE_URL = "https://api.bitfinex.com/"
    KEY=conf.BFX_KEY
    SECRET=conf.BFX_SECRET

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
            "content-type": "application/json",

            # "X-BFX-APIKEY":self.KEY,
            # "X-BFX-PAYLOAD":body,
            # "X-BFX-SIGNATURE":signature,

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
          print r.text
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
        try:
            url = "https://api.bitfinex.com/%s?%s" % (path, params)
            res = requests.get(url)
            # print '------16----->',res.text
            return json.loads(res.text)
        except Exception as e :
            print e
        return None

    # #取当前行情 (买卖价格)
    # def get_symb_tick(self, symb):
    #     # path = 'v2/ticker/%s' % symb
    #     # path = 'tickers'
    #     res =  self.api_get(path)
    #     print '------17----->',res
    #     if res :
    #         # 买 卖  最新
    #         return (float(res[0]), float(res[2]), float(res[6]) )
    #     else :
    #         return None

    #取当前行情 (买卖价格)
    def get_symb_tick(self, symb):
        symb = symb[1:]
        path = 'v1/pubticker/%s' % symb
        res =  self.api_get(path)
        print 'BFX ticker------------->', symb,  res
        if res :
            # 买 卖  最新
            return [ float(res['bid']), float(res['ask']), float(res['last_price']) ]
        else :
            return None
        
         
        

     #取当前行情订单
    def get_trades(self, symb):
        symb = self.getV1Symbol(symb)
        path = 'v1/trades/%s' % symb
        # path = 'tickers'
        res =  self.api_get(path)
        print '------19----->',res
        if res :
            return (float(res[0]), float(res[2]), float(res[6]))
        else :
            return None


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
     # [{'status': u'ACTIVE', 'price': 9, 'amount': 10, 'coin': u'EOS', 'side': 'buy', 'market': u'tEOSUSD'}]
    def get_act_orders(self):
        active_orders = []
        path = "v2/auth/r/orders"
        res = self.api_post(path = path)
        # print 'get_act_orders--------->',res
        for info in res :
            # symbols = info[3]
            odr = {}
            status = info[13]
            odr['status'] = status
            coin = info[3]
            # print 'coin---1------>',coin
            coin = coin[1:]
            coin = coin.replace('BTC','')
            coin = coin.replace('USD','')
            # print 'coin---2------>',coin
            odr['coin'] = coin
            odr['market'] = info[3]
            side = 'none'
            if info[6] > 0 :
                side = 'buy'
            if info[6] < 0 :
                side = 'sell'
            odr['side'] = side
            odr['price'] = info[16]
            odr['amount'] = info[7]
            
            active_orders.append(odr)

            # print 'symbols--------->',symbols
            # active_orders.append(symbols)
        return active_orders

    #余额
    def get_account_wallet(self):
        accounts = []
        path = "v2/auth/r/wallets"
        # path = "v1/balances"
        res = self.api_post(path = path)
        # print 'account_wallet------------->', res
        for info in res :
            way = info[0]
            if way == "exchange" :
                inf = {}
                inf['coin'] = info[1]
                inf['balance'] = float(info[2])
                accounts.append(inf)
        return accounts


    def getV1Symbol(self, sym):
        symbol = sym
        if symbol.startswith('t',0, 1):
            symbol = symbol[1:]
            symbol = symbol.lower()
        print 'symbol----------',symbol
        return symbol

    
    def get_balance(self):
        payload = {
            "request": "/v1/balances",
            "nonce": str(time.time()),
        }

        signed_payload = self._sign_payload(payload)
        r = requests.post(self.BASE_URL + "v1/balances", headers=signed_payload, verify=True)
        json_resp = r.json()

        try:
            if type(json_resp) is type([]):
                print "bfx get_balance----------success"
        except:
            return json_resp['message']

        return json_resp

    def new_order(self, amount, price, side,  symbol):
        symbol = self.getV1Symbol(symbol)

        payload = {
            'symbol':symbol,
            'amount':str(amount),
            'price':str(price),
            'side':side,
            'type':'exchange limit',
            'exchange':'bitfinex',  
            'ocoorder': False,
            'buy_price_oco': '0',
            'sell_price_oco': '0',
            "request": "/v1/order/new",
            "nonce": str(time.time()),

        }

        signed_payload = self._sign_payload(payload)
        r = requests.post(self.BASE_URL + "v1/order/new", headers=signed_payload, verify=True)
        json_resp = r.json()

        try:
            json_resp['order_id']
        except:
            return json_resp['message']

        return json_resp

    def _sign_payload(self, payload):
        j = json.dumps(payload)
        data = base64.standard_b64encode(j.encode('utf8'))

        h = hmac.new(self.SECRET.encode('utf8'), data, hashlib.sha384)
        signature = h.hexdigest()
        return {
            "X-BFX-APIKEY": self.KEY,
            "X-BFX-SIGNATURE": signature,
            "X-BFX-PAYLOAD": data
        }

    def outputJs(self, jspath, body):
        with open(jspath,'w') as fo :
            fo.write(body)
            fo.close()

if __name__ == "__main__":
    PLAT = 'bfx'
    markets={
        'btc/usdt':'tBTCUSD',
        'eos/usdt':'tEOSUSD',
        'eos/btc':'tEOSBTC',
        'ltc/usdt':'tLTCUSD',
        'ltc/btc':'tLTCBTC',
        'eth/usdt':'tETHUSD',
        'eth/btc':'tETHBTC',
        'etc/usdt':'tETCUSD',
        'etc/btc':'tETCBTC',
        'qtum/usdt':'tQTMUSD',
        'qtum/btc':'tQTMBTC',
        'xrp/usdt':'tXRPUSD',
        'xrp/btc':'tXRPBTC',
        }
    bfx = bfx_api()
    balance = bfx.get_symb_tick('tBTCUSD')
    print "--------",balance

    up_tm = int(time.time())
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "tamg", ["ticker","account","myorder","generator"])
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)
    
    for name, value in opts:
        #行情最新买卖价格
        if name in ('-t','--ticker'):
            print 'query--BFX----->ticker'
            banDao.createTicker()
            for mkt, symb in markets.items():
                # print mkt, "------>", symb
                ticker_price = bfx.get_symb_tick(symb)
                if ticker_price:
                    # to db
                    banDao.insertTicker(PLAT, up_tm, mkt.split('/')[0], mkt, ticker_price[0],ticker_price[1],ticker_price[2] )
                    # print "ticker_price----------->", ticker_price
                time.sleep(1)

        elif name in ('-a','--account'):
            print '>>> >>> query--BFX------->account'
            banDao.createAccount()
            balance_ls = bfx.get_balance()
            insert_ls = []
            for balance in balance_ls :
                ele ={
                    'coin':balance['currency'],
                    'balance':balance['available']
                }
                insert_ls.append(ele)
            banDao.insertAccount(PLAT, up_tm, insert_ls)
        elif name in ('-m','--myorder'):
            print '>>> >>> query--BFX------->myorder'
            banDao.createMyOrder()
            oders = bfx.get_act_orders()
            banDao.deleteMyOrder(PLAT)
            banDao.insertMyOrder(PLAT, up_tm, oders)

        elif name in ('-g','--generator'):
            data={}
            account={}
            myorder=""
            nginx_path = '/data/app/nginx/html/'
            tm_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            print 'curtm------->',tm_str

            #买卖信息
            for mkt, symb in markets.items() :
                # last = bz.getZbTicker(mkt)
                ticker = banDao.selectTicker(PLAT, mkt)
                mkt_js = mkt.replace("/","_")
                data[mkt_js] = ticker
                print ticker

                #
                coin = mkt.split('/')[0].upper();
                balance = banDao.selectCount(PLAT,coin)
                account[coin] = balance

                myord = banDao.selectMyOrderByPlat(PLAT)
                for ord in myord :
                    myorder += "<li>%s %s %s %s %s %s </li>" % (PLAT, ord['market'], ord['price'], ord['side'], ord['amount'] )


            data['up_tm'] = tm_str
            account['up_tm'] = tm_str

            temp_file = nginx_path + time.strftime("v2_bfx_%Y%m%d%H%M%S.js", time.localtime())
            outStr = """
            bfx_ticker = %s;
            bfx_account = %s;
            bfx_myorder = %s;
            """ % (json.dumps(data), json.dumps(account), myorder )
            bfx.outputJs(temp_file, outStr)

            subprocess.call("cp -rf " + temp_file + " " + nginx_path + "/v2_bfx.js", shell=True);
            subprocess.call("rm -rf " + temp_file , shell=True);
        else:
            print 'unhandled option'
            assert False, "unhandled option"

    # for mkt, symb in markets.items():
    #     print mkt,"------>",symb
    #     #市场的最新买卖价格
    #     ticker_price = bfx.get_symb_tick(symb)
    #     if ticker_price :
    #         #to db
    #         banDao.insertTicker(PLAT, up_tm, mkt.split('/')[0], mkt, ticker_price[0],ticker_price[1],ticker_price[2] )
    #         print "ticker_price----------->", ticker_price

    # banDao.selectTickers(PLAT)

    #行情订单
    # bfx.get_trades(markets['eos/usd'])


    # #账户信息
    # banDao.createAccount()
    # accountDic = bfx.get_account_wallet()
    # banDao.insertAccount(PLAT, up_tm, accountDic)
    # banDao.selectCount('BTC')


    # # 我的订单信息
    # banDao.createMyOrder()
    # myOdrLs = bfx.get_act_orders()
    # print 'myOdrLs-----------------', myOdrLs
    # banDao.insertMyOrder(PLAT, up_tm, myOdrLs)
    # banDao.selectMyOrder(PLAT)


    #创建订单
    # print '===>', bfx.new_order('13','8','buy','exchange limit', markets['eos/usd'])





    

    


    
