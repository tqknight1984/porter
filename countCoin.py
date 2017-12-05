#!/usr/bin/python
# -*- coding: utf-8 -*- 


import sys

from wxStart import WxStart
from yunUtil import YunUtil
from szzc import szzcUtil

from yunbi.client import Client, get_api_path
from yunbi.conf import ACCESS_KEY, SECRET_KEY

class CountCoin():
    def __init__(self):
        print "---> CountCoin.init()"


if __name__ == '__main__':
    
    SZZC_KK = 100000000

    arg_len = len(sys.argv)
    if arg_len < 2:
        print u'参数有误-->请输入需要查询的数字币'
        exit(1)


    wxStart = WxStart()

    # if (len(sys.argv) == 2):
    #     print u"查询%s数量 " % sys.argv[1]
    # else :
    #     print u'参数有误-->请输入需要查询的数字币'
    #     exit(1)
    yunbi = YunUtil()

    #yunbi
    yunbi_info = yunbi.getMebersInfo()
    print u'yunbi_info------->', yunbi_info, '\n'
    if yunbi_info == None :
        wxStart.sendSms('tq', (u"yunbi: request failed!!! >>> count " + (" ".join(sys.argv[1:]))), "#0000FF")
        exit(1)

    #szzc
    szzc_info = szzcUtil.list_balances()
    print u'szzc_info------->', szzc_info, '\n'
    if szzc_info == None :
        wxStart.sendSms('tq', (u"szzc: request failed!!! >>> count " + (" ".join(sys.argv[1:]))), "#0000FF")
        exit(1)

    if yunbi_info['activated'] and szzc_info['status']['success'] == 1 : 
        msgStr = u""

        # yun cny
        accounts = yunbi_info['accounts']
        for account in accounts:
            if account['currency'] == 'cny':
                cny = float(account['balance'])
                msgStr = u"%s yun:cny:%.2f;" % (msgStr, cny)

        # szzc cny
        szzc_accounts = szzc_info['result']
        for account in szzc_accounts:
            if account['asset'] == 'CNY':
                cny = float(account['balance'])/SZZC_KK
                msgStr = u"%s szzc:cny:%.2f;" % (msgStr, cny)

        # coins
        for i in range (1, arg_len):
            coin = sys.argv[i]

            # print coin
            if coin :
                # yunbi
                for account in accounts:
                    if account['currency'] == coin.lower():
                        num = float(account['balance'])
                        msgStr = u"%s yun:%s:%.2f;" % (msgStr, coin, num)

                # szzc
                for account in szzc_accounts:
                    if account['asset'] == coin.upper():
                        num = float(account['balance'])/SZZC_KK
                        msgStr = u"%s szzc:%s:%.2f;" % (msgStr, coin, num)
        
        print msgStr
        #
        
        wxStart.sendSms('tq', msgStr, "#0000FF")
    


