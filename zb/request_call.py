#coding=utf-8
import requests,hashlib,hmac,decimal,time,collections

reload(sys)
sys.setdefaultencoding('utf-8')

proxies = {"https": "https://127.0.0.1:1080"}  #这里是你代理科学上网的端口
timeout=1
class request_call(object):

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
    @staticmethod
    def zb_proxy_call(host,payload):
        try:
            response=requests.get(host,payload,proxies=proxies,timeout=timeout)
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
