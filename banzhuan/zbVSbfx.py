# coding=utf-8
import sys
import requests
import json
import os
import time
import subprocess
from request_call import request_call

from banDao import banDao
from zb_api import zb_api
from bfx_api import bfx_api
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
        res =  request_call.zb_proxy_call(url,payload)
        if res :
            return res.get('id', None)
        return None

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
        print 'orders-----------',orders
        # coin = odrDic['coin']
        #     market = odrDic['market']
        #     side = odrDic['side']
        #     amount = odrDic['amount']
        #     price = odrDic['price']
        res = []
        if orders :
            for odr in orders :
                #status : 挂单状态(0：待成交,1：取消,2：交易完成,3：待成交未交易部份)
                if odr['status'] == 2 or odr['status'] == 1 :
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
                    'amount':odr['total_amount'],
                    'price':odr['price'],
                }
                res.append(ele)
        return res



if __name__ == "__main__":
    zb_plat='zb'
    bfx_plat='bfx'
    ban_ls=[
        # {   
        # 'market':'btc/usdt',
        # 'zb_symb':'btc_usdt',
        # 'bfx_symb':'tBTCUSD',
        # 'direction':'zb2bfx',
        # 'limit_perc':10,
        # 'trade_amount':0.2,
        # 'margin_perc':0.05,
        # },
        {   
        'market':'eos/usdt',
        'zb_symb':'eos_usdt',
        'bfx_symb':'tEOSUSD',
        'direction':'zb2bfx',
        'limit_perc':10,
        'trade_amount':10.0,
        'margin_perc':0.05,
        },
    ]
   

    up_tm = int(time.time())
    print 'curtm------->', up_tm

    for ban_ele in ban_ls :
        market = ban_ele['market']
        coin = market.split('/')[0]
        zb_symb = ban_ele['zb_symb']
        bfx_symb = ban_ele['bfx_symb']
        direction = ban_ele['direction']
        limit_perc = ban_ele['limit_perc']
        trade_amount = ban_ele['trade_amount']
        margin_perc = ban_ele['margin_perc']

        ban_flag = 0
        zb_trick = banDao.selectTicker(zb_plat,market)
        bfx_trick = banDao.selectTicker(bfx_plat,market)

        #差价条件
        if ban_flag == 0 :
            if zb_trick and bfx_trick :
                #比较差价 zb sell and bfx buy
                if direction == 'zb2bfx' :
                    off = zb_trick[1] - bfx_trick[0]
                    avg = (zb_trick[1] + bfx_trick[0]) / 2
                    perc = 100 * off / avg
                    if perc >= limit_perc :
                        ban_flag = 1
                    else :
                        print u'%s差价 %s , %s < %s 不通过' % (market, off, prec , limit_prec)
        
        if ban_flag != 1 and ban_flag != 2 :
            print u'差价条件不通过', market
            continue


        #是否有未完成的挂单
        if ban_flag == 1 :
            myods = banDao.selectMyOrder(coin)
            print u'myods-------------->%s' % (len(myods))
            if len(myods) == 0 :
                ban_flag = 3
                


        if ban_flag != 3 and ban_flag != 4 :
            print u'有未完成的挂单', market
            continue

        zb_account = banDao.selectCount(zb_plat, market.split('/')[0])
        bfx_account = banDao.selectCount(bfx_plat, market.split('/')[1])

        #账户条件
        if ban_flag == 3 :
            if direction == 'zb2bfx' :
                if zb_account >= trade_amount:
                    if bfx_account >= (bfx_trick[0] * trade_amount) :
                        ban_flag = 5


        if ban_flag != 5 and ban_flag != 6 :
            print u'账户条件不通过', market
            continue

        if ban_flag == 5 :
            sell_price = zb_trick[1] - (zb_trick[1] *  margin_perc)
            if sell_price > 0 :
                # sell_id = zb_api().new_order(zb_symb, sell_price, trade_amount, 'sell')
                sell_id = 1
                print (u'>>> >>> 挂单 ZB %s %s sell %s个 ' % (zb_symb, sell_price, trade_amount))
                if sell_id > 0 :
                    buy_price = bfx_trick[0] + (bfx_trick[0] * margin_perc)
                    # buy_id = bfx_api().new_order(trade_amount, buy_price,'buy', bfx_symb)
                    buy_id = 1
                    print (u'>>> >>> 挂单 BFX %s %s buy %s个 ' % (bfx_symb, buy_price, trade_amount))
                    if buy_id > 0 :
                        ban_flag =7

        if ban_flag != 7 and ban_flag != 8 :
            print u'挂单失败', market
            continue

                
                
                
            


                        
                    
            
            
        #取两边最新价格，判断谁买谁卖

        #判断差价是否满足要求

        #判断最新买价卖价的差价

        #判断是否有足够的币，足够的usdt，btc

