import gevent
from request_call import request_call
#
#交易类
#
class zb_api_trade(request_call):

    def __init__(self):
        self.access_key=''  #你的key
        self.access_secret='' #你的secret
        self.host='https://trade.zb.com/api'


    #获取用户信息
    def get_account_info(self):
        dict={"method":"getAccountInfo","accesskey":str(self.access_key)}
        url=self.host+'/getAccountInfo'
        signature=self.zb_signature(dict)
        payload=self.add_sign_retime(dict,signature,self.milliseconds())
        return  request_call.zb_proxy_call(url,payload)
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
    #获取委托买单或卖单
    def get_oder(self,currency,id):
        dict={"accesskey":str(self.access_key),'currency':currency,'id':id,'method':'getOrder'}
        url=self.host+'/getOrder'
        signature=self.zb_signature(dict)
        payload=self.add_sign_retime(dict,signature,self.milliseconds())
        return  request_call.zb_proxy_call(url,payload)
    #获取多个委托买单或卖单，每次请求返回10条记录
    def get_oders(self,currency,pageIndex,tradeType):
        dict={"accesskey":str(self.access_key),'currency':currency,'pageIndex':pageIndex,'tradeType':tradeType,'method':'getOrders'}
        url=self.host+'/getOrders'
        signature=self.zb_signature(dict)
        payload=self.add_sign_retime(dict,signature,self.milliseconds())
        return  request_call.zb_proxy_call(url,payload)
    #(新)获取多个委托买单或卖单，每次请求返回pageSize<100条记录
    def get_orders_new(self,currency,pageIndex,pageSize,tradeType):
        dict={"accesskey":str(self.access_key),'currency':currency,'pageIndex':pageIndex,'pageSize':pageSize,'tradeType':tradeType,'method':'getOrdersNew'}
        url=self.host+'/getOrdersNew'
        signature=self.zb_signature(dict)
        payload=self.add_sign_retime(dict,signature,self.milliseconds())
        return  request_call.zb_proxy_call(url,payload)
    #与getOrdersNew的区别是取消tradeType字段过滤，可同时获取买单和卖单，每次请求返回pageSize<100条记录
    def get_orders_ignore_tradeType(self,currency,pageIndex,pageSize):
        dict={"accesskey":str(self.access_key),'currency':currency,'pageIndex':pageIndex,'pageSize':pageSize,'method':'getOrdersIgnoreTradeType'}
        url=self.host+'/getOrdersIgnoreTradeType'
        signature=self.zb_signature(dict)
        payload=self.add_sign_retime(dict,signature,self.milliseconds())
        return  request_call.zb_proxy_call(url,payload)

    #获取未成交或部份成交的买单和卖单，每次请求返回pageSize<=10条记录
    def get_unfinished_orders_ignore_tradeType(self,currency,pageIndex,pageSize):
        dict={"accesskey":str(self.access_key),'currency':currency,'pageIndex':pageIndex,'pageSize':pageSize,'method':'getUnfinishedOrdersIgnoreTradeType'}
        url=self.host+'/getUnfinishedOrdersIgnoreTradeType'
        signature=self.zb_signature(dict)
        payload=self.add_sign_retime(dict,signature,self.milliseconds())
        return  request_call.zb_proxy_call(url,payload)
    #获取用户充值地址
    def get_user_address(self,currency):
        dict={"accesskey":str(self.access_key),'currency':currency,'method':'getUserAddress'}
        url=self.host+'/getUserAddress'
        signature=self.zb_signature(dict)
        payload=self.add_sign_retime(dict,signature,self.milliseconds())
        return  request_call.zb_proxy_call(url,payload)
    #获取用户认证的提现地址
    def get_withdraw_address(self,currency):
        dict={"accesskey":str(self.access_key),'currency':currency,'method':'getWithdrawAddress'}
        url=self.host+'/getWithdrawAddress'
        signature=self.zb_signature(dict)
        payload=self.add_sign_retime(dict,signature,self.milliseconds())
        return  request_call.zb_proxy_call(url,payload)
    #获取数字资产提现记录
    def get_withdraw_record(self,currency):
        dict={"accesskey":str(self.access_key),'currency':currency,'method':'getWithdrawRecord'}
        url=self.host+'/getWithdrawRecord'
        signature=self.zb_signature(dict)
        payload=self.add_sign_retime(dict,signature,self.milliseconds())
        return  request_call.zb_proxy_call(url,payload)
    #获取数字资产充值记录
    def get_charge_record(self,currency,pageIndex,pageSize):
        dict={"accesskey":str(self.access_key),'currency':currency,'pageIndex':pageIndex,'pageSize':pageSize,'method':'getChargeRecord'}
        url=self.host+'/getChargeRecord'
        signature=self.zb_signature(dict)
        payload=self.add_sign_retime(dict,signature,self.milliseconds())
        return  request_call.zb_proxy_call(url,payload)
    #提现
    def withdraw(self,currency,fees,itransfer,receiveAdrr,sagePwd):
        dict={"accesskey":str(self.access_key),'currency':currency,'fees':fees,'itransfer':itransfer,'receiveAdrr':receiveAdrr,'sagePwd':sagePwd,'method':'withdraw'}
        url=self.host+'/withdraw'
        signature=self.zb_signature(dict)
        payload=self.add_sign_retime(dict,signature,self.milliseconds())
        return  request_call.zb_proxy_call(url,payload)



    #签名
    def zb_signature(self,dict):
        map=request_call.order_by_parme(dict)
        orderbyparme=self.parme_to_sign_string(map)
        secret=request_call.sha1(self.access_secret.encode('utf8'))
        signature=request_call.hmac_sign(orderbyparme.encode('utf-8'),secret.encode('utf-8'))
        return  signature

    #获取毫秒
    def get_milliseconds(self):
        return self.milliseconds()

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

    @staticmethod
    def return_code_message(code):
        if code==1000:
            print("购买成功")
        elif code==1001:
            print('一般错误提示')
        elif code==1002:
            print('内部错误')
        elif code==1003:
            print('验证不通过')
        elif code==1004:
            print('资金安全密码锁定')
        elif code==1005:
            print('资金安全密码错误，请确认后重新输入。')
        elif code==1006:
            print('实名认证等待审核或审核不通过')
        elif code==1005:
            print('资金安全密码错误，请确认后重新输入。')
        elif code==1009:
            print('此接口维护中')
        elif code==2001:
            print('人民币账户余额不足')
        elif code==2002:
            print('比特币账户余额不足')
        elif code==2003:
            print('莱特币账户余额不足')
        elif code==2005:
            print('以太币账户余额不足')
        elif code==2006:
            print('ETC币账户余额不足')
        elif code==2007:
            print('BTS币账户余额不足')
        elif code==2009:
            print('账户余额不足')
        elif code==3001:
            print('挂单没有找到')
        elif code==3002:
            print('无效的金额')
        elif code==3003:
            print('无效的数量')
        elif code==3004:
            print('用户不存在')
        elif code==3005:
            print('无效的参数')
        elif code==3006:
            print('无效的IP或与绑定的IP不一致')
        elif code==3007:
            print('请求时间已失效')
        elif code==3008:
            print('交易记录没有找到')
        elif code==4001:
            print('API接口被锁定或未启用')
        elif code==4002:
            print('请求过于频繁')
if __name__ == '__main__':
    loop=gevent.get_hub().loop #定时任务
    task=loop.timer(0.0,1) #1秒钟执行一次
    a=zb_api_trade("btc_usdt")
    task.start(a.get_account_info)

    loop.run()








