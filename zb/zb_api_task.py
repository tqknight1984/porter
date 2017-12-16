import time,gevent,decimal
from zb_api_data import zb_api_data
from zb_api_trade import zb_api_trade

list=[]
isMoney=0
class zb_api_task():
    def __init__(self,currency,isOder):
        self.currency=currency
        self.isOreder=isOder


    def get_ticker_message(self):
        api=zb_api_data(self.currency)
        map=api.ticker()
        if map is not None:
            date=map['date']
            high=float(map["ticker"]["high"])
            low=float(map["ticker"]["low"])
            buy=float(map["ticker"]["buy"])
            sell=float(map["ticker"]["sell"])
            t=self.time_format(date)
            usdt=map["ticker"]["last"]
            vol=map["ticker"]["vol"]
            u=float(usdt)
            print("【%s】 =================================================="%(t))
            str="             "
            self.mean_point(high,low,u)
            di=self.differ(buy,sell)
            lowD=self.low_differ(low,u)
            highD=self.high_differ(high,u)
            print(('%s买卖相差价:%s ')%(str,di))
            print(('%s距离最高价:%s | 距离最低价：%s')%(str,highD,lowD))

            s=str+"最高价:%s  | 最低价:%s\n%s买一价:%s | 卖一价:%s\n%s成交价:%s 成交量:%s" \
                  %(high,low,str,buy,sell,str,usdt,vol)
            print(s)
            # if(isMoney):
            #  buyP=buy+0.01
            #  self.buy_order_btc(di,highD,buyP)
            print("          %s==================================================\n"%("   "))
        else:
            print("获取数据失败")
    #time:yyyy-mm-dd hh:mm:ss 13位需要除以1000
    def time_format(self,date):
        t=float(int(date)/1000)
        return time.strftime('%H:%M:%S', time.localtime(t))
    #平均价
    def mean_point(self,high,low,last):
        str="             "
        point=float(high+low)/2
        print("%s平均点:%s" %(str,point))
        p=float(last-point)
        money=self.decimal(p,"0000.00")
        if (last>p):
            print("%s交易点在平均点上:%s" %(str,money))
        if(last<p):
            print("%s交易点在平均点下:%s" %(str,money))
        if(p==last):
            print("%s交易点等于平均点:%" %(str,money))
    #买入
    def buy_order_btc(self,di,highD,price):
        str="             "
        if highD<150:
            print("%s距离最高点只差150，危险中"%(str))
        else:
         if di>20:
            print('%s买卖差价大过20，不适合买入'%(str))
         else:
          amount=0.001

          t=zb_api_trade()
          return self.response_oder(t.request_order(self.currency,price,amount,1))

    #保存订单号
    def response_oder(self,map):
        if map is not None:
           code=  map['code']
           zb_api_trade.return_code_message(code)
           if code=='1000':
               list.append(id)
        else:
           return None
    #是否有钱
    @staticmethod
    def is_money():
     t=  zb_api_trade()
     map=  t.get_account_info()
     if map is not None:
      coins=map['result']['coins'][0]
      print(coins)
      available=int(coins['available'])
      print(available)
      if int(available)>=20:
         return 1
      else:
         return 0










    #买卖相差价钱
    def differ(self,buy,sell):
        d= float(sell-buy)
        return self.decimal(d,"00.00")
    #距离最高点
    def high_differ(self,hight,last):
        d=float(hight-last)
        return self.decimal(d,'00.00')
    #距离低点
    def low_differ(self,low,last):
        d=float(last-low)
        return self.decimal(d,'00.00')
    #货币换算

    def decimal(self,money,digit):
        return decimal.Decimal(money).quantize(decimal.Decimal(digit))
if __name__ == '__main__':
    loop=gevent.get_hub().loop #定时任务
    task=loop.timer(0.0,1) #1秒钟执行一次
    isMoney=0
    a=zb_api_task('btc_usdt',isMoney)
    task.start(a.get_ticker_message)
    loop.run()