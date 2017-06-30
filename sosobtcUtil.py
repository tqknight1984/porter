#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import requests
import bs4
import json
import string
import time


class SosobtcUtil():
    # xx_off可以是绝对值也可以是百分比（<1）

    def __init__(self, zec_off=8, eth_off=6):
        # self.access_key = access_key
        self._zec_off = zec_off
        self._eth_off = eth_off
        print "SosobtcUtil.init()"

    def getSosoData(self):
        response = requests.get('https://www.sosobtc.com/')
        begin = response.text.find("window.__data=") + len("window.__data=")
        end = response.text[begin:].find(";</script>")
        soso_data = response.text[begin:begin + end]
        soso_json = json.loads(soso_data)
        return soso_json

    def getCoinInfo(self, coins):
        soso_json = self.getSosoData()
        infos = {}
        for coin in coins: 
            yunbi_str = '0.00'
            szzc_str = '0.00'
            if (coin + ':yunbi')in soso_json['root']['tickers'].keys() :
                yunbi_str = soso_json['root']['tickers'][coin + ':yunbi']['last']
            if (coin + ':szzc')in soso_json['root']['tickers'].keys() :
                szzc_str = soso_json['root']['tickers'][coin + ':szzc']['last']
            yunbi = float(yunbi_str)
            szzc = float(szzc_str)
            off = szzc - yunbi
            off_str = u"%s: %.2f(szzc) - %.2f(yunbi) = %.2f" % (coin, szzc, yunbi, off)
            # print u"计算-------> %s" % (off_str)
            # off_item = (coin, off, off_str)
            item = {}
            item['yunbi']=yunbi
            item['szzc']=szzc
            item['soso_offv'] = off
            item['notify_str'] = off_str
            infos[coin] = item
        return infos


    def getOff(self):
        response = requests.get('https://www.sosobtc.com/')

        # soup = bs4.BeautifulSoup(response.text)
        # zcashStr = soup.find("span", { "data-reactid" : "300" })
        # open("zzz.txt","w+").write(response.text.encode('utf-8'))

        begin = response.text.find("window.__data=") + len("window.__data=")
        end = response.text[begin:].find(";</script>")
        # print  "1--->"+str(begin)
        # print  "2--->"+str(end)
        # print  "3--->"+str(end - begin)
        hfd_data = response.text[begin:begin + end]

        # print hfd_data[-10:]

        hfd_json = json.loads(hfd_data)

        str_sms = ''

# zec
        yunbi_str = hfd_json['root']['tickers']['zec:yunbi']['last']
        szzc_str = hfd_json['root']['tickers']['zec:szzc']['last']

        yunbi = float(yunbi_str)
        szzc = float(szzc_str)

# 价格过低预警
        if(yunbi < 390 or szzc < 390):
            str_sms = u"zec:价格过底：%s(szzc), %s(yunbi)" % (szzc_str, yunbi_str)

# 差价预警
        off = szzc - yunbi
        print "-->zec:%s(szzc) - %s(yunbi) = %s" % (szzc_str, yunbi_str, off)
        if self._zec_off > 1:
            print "-->zec_limit:%s" % (self._zec_off)
            if off > self._zec_off or off < -self._zec_off:
                str_sms = "zec:%s(szzc) - %s(yunbi) = %s" % (szzc_str,
                                                             yunbi_str, off)
        else:
            off_limit = (szzc + yunbi) / 2 * self._zec_off
            print "-->zec_limit:%s" % (off_limit)
            if off > off_limit or off < -off_limit:
                str_sms = "zec:%s(szzc) - %s(yunbi) = %s" % (szzc_str,
                                                             yunbi_str, off)


# eth
        yunbi_str = hfd_json['root']['tickers']['eth:yunbi']['last']
        szzc_str = hfd_json['root']['tickers']['eth:szzc']['last']

        yunbi = float(yunbi_str)
        szzc = float(szzc_str)

# 价格过低预警
        if(yunbi < 300 or szzc < 300):
            str_sms = u"\n%s eth:价格过底：%s(szzc), %s(yunbi)" % (
                str_sms, szzc_str, yunbi_str)

# 差价预警
        off = szzc - yunbi
        print "-->eth:%s(szzc) - %s(yunbi) = %s" % (szzc_str, yunbi_str, off)
        if self._eth_off > 1:
            print "-->eth_limit:%s" % (self._eth_off)
            if off > self._eth_off or off < -self._eth_off:
                str_sms = "\n%s eth:%s(szzc) - %s(yunbi) = %s" % (str_sms,
                                                                  szzc_str, yunbi_str, off)
        else:
            off_limit = (szzc + yunbi) / 2 * self._eth_off
            print "-->eth_limit:%s" % (off_limit)
            if off > off_limit or off < -off_limit:
                str_sms = "\n%s eth:%s(szzc) - %s(yunbi) = %s" % (str_sms,
                                                                  szzc_str, yunbi_str, off)

        print 'str_sms-->' + str_sms
        return str_sms
        # print szzc_str+"(szzc) - "+yunbi_str+"(yunbi) = "+str(off)
        # return off
    # print hfd_json['tickers']


# while True:
#     off = SosobtcUtil().getOff()
#     time.sleep( 10 )
#     # print "off-------> %s",off
# # zec:yunbi
