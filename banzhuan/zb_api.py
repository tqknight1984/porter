# coding=utf-8
import sys
import requests
import json
import os
import time
import subprocess
from request_call import request_call

from banDao import banDao
import conf

reload(sys)
sys.setdefaultencoding('utf-8')

timeout = 3


class zb_api:
    def __init__(self):
        self.access_key=conf.ZB_KEY
        self.access_secret=conf.ZB_SECRET
        self.host='https://trade.zb.com/api'

    def api_get(self, path, params=''):
        url = 'http://api.zb.com/%s?%s' % (path, params)
        try:
            res = requests.get(url, timeout=timeout)
            jo = json.loads(res.content)
            print ' jo------------->', jo
            if jo:
                return jo
            else:
                return None
        except requests.Timeout as e:
            print e

    # 获取行情价
    def getZbTicker(self, market):
        jo = self.api_get('data/v1/ticker', 'market=%s' % market)
        ticker = jo.get("ticker", None)
        if ticker:
            return (ticker['buy'], ticker['sell'], ticker['last'])
        else:
            return None


    #拼接签名字符串
    def parme_to_sign_string(self,map):
        if map is not None:
            stri=""
            for k, v in map.items():
                stri +='%s=%s%s' %(k,v,"&")
            return  stri.strip('&')
        else:
            return None

#追加参数
    def add_sign_retime(self,dict,sign,retime):
        dict['sign']=sign
        dict["reqTime"]=retime
        return dict

    #签名
    def zb_signature(self,dict):
        map=request_call.order_by_parme(dict)
        orderbyparme=self.parme_to_sign_string(map)
        secret=request_call.sha1(self.access_secret.encode('utf8'))
        signature=request_call.hmac_sign(orderbyparme.encode('utf-8'),secret.encode('utf-8'))
        return  signature

        #签名
    @staticmethod
    def hmac_sign(auth,secret):
        h=hmac.new(secret,auth,hashlib.md5)
        return h.hexdigest()

    #sha1加密
    @staticmethod
    def sha1(secret):
        h=hashlib.new('sha1',secret)
        return h.hexdigest()

    #货币换算
    @staticmethod
    def decimal(number):
        return str(decimal.Decimal(str(number)))
    #毫秒
    @staticmethod
    def milliseconds():
        return str(int(time.time() * 1000))
    #参数排序返回字符串
    @staticmethod
    def order_by_parme(dic):
        return collections.OrderedDict(sorted(dic.items(), key=lambda t: t[0]))


    @staticmethod
    def zb_call(host,payload):
        try:
            response=requests.get(host,payload,timeout=timeout)
            response.raise_for_status()
            return  response.json()
        except requests.Timeout as  e:
            print(e)

        except requests.HTTPError as e:
            print(e)

        except requests.ConnectionError as e:
            print(e)

        except ValueError as e:
            print(e)
    #获取用户信息
    def get_account_info(self):
        dict={"method":"getAccountInfo","accesskey":str(self.access_key)}
        url=self.host+'/getAccountInfo'
        signature=self.zb_signature(dict)
        payload=self.add_sign_retime(dict,signature,self.milliseconds())
        info = request_call.zb_call(url,payload)
        # print '--result---------->',info['result']
        # print '--coins---------->',info['result']['coins']

        accounts = []
        if info :
            coins = info['result']['coins']
            for inf in coins :
                # print inf['enName'], '-------------',  inf['available']
                ele = {}
                ele['coin'] = inf['enName']
                ele['balance'] = inf['available']
                accounts.append(ele)

        return accounts


    #委托下单
    def request_order(self,currency,price,amount,tradeType):
        dict={"accesskey":str(self.access_key),"currency":currency,"price":price,"amount":amount,"tradeType":tradeType,"method":"order"}
        url=self.host+'/order'
        signature=self.zb_signature(dict)
        payload=self.add_sign_retime(dict,signature,self.milliseconds())
        return  request_call.zb_proxy_call(url,payload)

    #取消委托
    def cancel_order(self,currency,id):
        dict={"accesskey":str(self.access_key),'currency':currency,'id':id,'method':'cancelOrder'}
        url=self.host+'/cancelOrder'
        signature=self.zb_signature(dict)
        payload=self.add_sign_retime(dict,signature,self.milliseconds())
        return  request_call.zb_proxy_call(url,payload)


    #获取多个委托买单或卖单，每次请求返回10条记录
    def get_oders(self,currency,pageIndex=1,tradeType=1):
        dict={"accesskey":str(self.access_key),'currency':currency,'pageIndex':pageIndex,'tradeType':tradeType,'method':'getOrders'}
        url=self.host+'/getOrders'
        signature=self.zb_signature(dict)
        payload=self.add_sign_retime(dict,signature,self.milliseconds())
        orders = request_call.zb_proxy_call(url,payload)

        # coin = odrDic['coin']
        #     market = odrDic['market']
        #     side = odrDic['side']
        #     amount = odrDic['amount']
        #     price = odrDic['price']
        res = []
        if orders :
            for odr in orders :
                #status : 挂单状态(0：待成交,1：取消,2：交易完成,3：待成交未交易部份)
                if odr['status'] == 2 :
                    continue                
                currency = odr['currency']
                coin = currency[0: currency.index('_')]
                print 'coin-----------',coin
                market = currency.replace('_','/')
                print 'market-----------',market
                side = 'zzz'
                if odr['type'] == 0:
                    side = 'sell'
                if odr['type'] == 1:
                    side = 'buy'

                ele = {
                    'coin':coin,
                    'market':market,
                    'side':side,
                    'amount':odr['trade_amount'],
                    'price':odr['price'],
                }

                res.append(ele)
        return res



if __name__ == "__main__":
    PLAT = 'zb'
    markets = {
        'btc/usdt': 'btc_usdt',
        'bcc/usdt': 'bcc_usdt',
        'bcc/btc': 'bcc_usdt',
        'ltc/usdt': 'ltc_usdt',
        'ltc/btc': 'ltc_btc',
        'eos/usdt': 'eos_usdt',
        'eos/btc': 'eos_btc',
        'eth/usdt': 'eth_usdt',
        'eth/btc': 'eth_btc',
        'etc/usdt': 'etc_usdt',
        'etc/btc': 'etc_btc',
        'qtum/usdt': 'qtum_usdt',
        'qtum/btc': 'qtum_btc',
        'xrp/usdt': 'xrp_usdt',
        'xrp/btc': 'xrp_btc',
    }

    zb = zb_api()

    banDao.createTicker()

    up_tm = int(time.time())
    print 'curtm------->', up_tm


    # #行情最新买卖价格
    # for mkt, symb in markets.items():
    #     print mkt, "------>", symb
    #     # 市场的最新买卖价格
    #     ticker_price = zb.getZbTicker(symb)
    #     if ticker_price:
    #         # to db
    #         banDao.insertTicker(PLAT, up_tm, mkt.split('/')[0], mkt, ticker_price[0], ticker_price[1], ticker_price[2])
    #         print "ticker_price----------->", ticker_price

    # banDao.selectTickers(PLAT)



    # #账户信息
    # banDao.createAccount()
    # accountDic = zb.get_account_info()
    # print "accountDic----------->", accountDic
    # banDao.insertAccount(PLAT, up_tm, accountDic)
    # banDao.selectCount('BTC')

     # 获取委托买单或卖单
    banDao.createMyOrder()
    oders = zb.get_oders(markets['eos/usdt'])
    print 'oders-----------------', oders
    banDao.insertMyOrder(PLAT, up_tm, oders)
    banDao.selectMyOrder(PLAT)
