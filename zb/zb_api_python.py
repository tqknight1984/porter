import json, urllib2, hashlib,struct,sha,time,sys

class zb_api:
	
    def __init__(self, mykey, mysecret):
        self.mykey    = mykey
        self.mysecret = mysecret

    def __fill(self, value, lenght, fillByte):
        if len(value) >= lenght:
            return value
        else:
            fillSize = lenght - len(value)
        return value + chr(fillByte) * fillSize

    def __doXOr(self, s, value):
        slist = list(s)
        for index in xrange(len(slist)):
            slist[index] = chr(ord(slist[index]) ^ value)
        return "".join(slist)

    def __hmacSign(self, aValue, aKey):
        keyb   = struct.pack("%ds" % len(aKey), aKey)
        value  = struct.pack("%ds" % len(aValue), aValue)
        k_ipad = self.__doXOr(keyb, 0x36)
        k_opad = self.__doXOr(keyb, 0x5c)
        k_ipad = self.__fill(k_ipad, 64, 54)
        k_opad = self.__fill(k_opad, 64, 92)
        m = hashlib.md5()
        m.update(k_ipad)
        m.update(value)
        dg = m.digest()
        
        m = hashlib.md5()
        m.update(k_opad)
        subStr = dg[0:16]
        m.update(subStr)
        dg = m.hexdigest()
        return dg

    def __digest(self, aValue):
        value  = struct.pack("%ds" % len(aValue), aValue)
        # print value
        h = sha.new()
        h.update(value)
        dg = h.hexdigest()
        return dg

    def api_call(self, path, params = ''):
        try:
            url = 'http://api.zb.com/data/v1/' + path + '?' + params
            request = urllib2.Request(url)
            response = urllib2.urlopen(request, timeout=5)
            doc = json.loads(response.read())
            return doc
        except Exception,ex:
            print >>sys.stderr, 'zb request ex: ', ex
            return None


    def __api_call(self, path, params = ''):
        try:
            SHA_secret = self.__digest(self.mysecret)
            sign = self.__hmacSign(params, SHA_secret)
            reqTime = (int)(time.time()*1000)
            params+= '&sign=%s&reqTime=%d'%(sign, reqTime)
            url = 'https://trade.zb.com/api/' + path + '?' + params
            request = urllib2.Request(url)
            response = urllib2.urlopen(request, timeout=5)
            doc = json.loads(response.read())
            return doc
        except Exception,ex:
            print >>sys.stderr, 'zb request ex: ', ex
            return None

    def query_account(self):
        try:
            params = "accesskey="+self.mykey+"&method=getAccountInfo"
            path = 'getAccountInfo'
            
            obj = self.__api_call(path, params)
            #print obj
            return obj
        except Exception,ex:
            print >>sys.stderr, 'zb query_account exception,',ex
            return None

    def getOrders(self, currency):
        try:
            params = "accesskey="+self.mykey+"&currency="+currency+"&method=getOrders&pageIndex=1&tradeType=1"
            print params
            path = 'getOrders'
            
            obj = self.__api_call(path, params)
            #print obj
            return obj
        except Exception,ex:
            print >>sys.stderr, 'zb getOrders exception,',ex
            return None

    def getOrdersNew(self):
        try:
            params = "accesskey="+self.mykey+"&currency=etc_usdt&method=getOrdersNew&pageIndex=1&pageSize=1&tradeType=1"
            path = 'getOrdersNew'
            
            obj = self.__api_call(path, params)
            #print obj
            return obj
        except Exception,ex:
            print >>sys.stderr, 'zb getOrdersNew exception,',ex
            return None

    def getOrdersIgnoreTradeType(self):
        try:
            params = "accesskey="+self.mykey+"&currency=etc_usdt&method=getOrdersIgnoreTradeType&pageIndex=1&pageSize=1"
            path = 'getOrdersIgnoreTradeType'
            
            obj = self.__api_call(path, params)
            #print obj
            return obj
        except Exception,ex:
            print >>sys.stderr, 'zb getOrdersNew exception,',ex
            return None

    def getAccountInfo(self):
        try:
            params = "accesskey="+self.mykey+"&method=getAccountInfo"
            path = 'getAccountInfo'
            
            obj = self.__api_call(path, params)
            #print obj
            return obj
        except Exception,ex:
            print >>sys.stderr, 'zb getOrdersNew exception,',ex
            return None


        
if __name__ == '__main__':
    access_key    = ''
    access_secret = ''

    api = zb_api(access_key, access_secret)

    print (api.api_call("ticker", "market=btc_usdt"))

    # print api.query_account()
    # print api.getOrders("etc_btc")
    # print api.getOrdersNew()
    # print api.getOrdersIgnoreTradeType()
    print api.getAccountInfo()
        