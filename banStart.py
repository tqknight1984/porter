#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import json
import time
import os

import szzc.szzcUtil as szzcUtil
from sosobtcUtil import SosobtcUtil
from yunUtil import YunUtil
# from szzc import szzcUtil
from confUtil import ConfUtil
from fileReadUtil import FileReadUtil

appid = 'wx5d2607e7bf434326'
secrect = '6a005490e16bae05e256e06ebf3118db'

class BanStart():

    def __init__(self):
        self.appid = appid
        self.secrect = secrect
# 获取accessToken

    def getToken(self):
        # 判断缓存
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + self.appid + "&secret=" + self.secrect
        # print "getToken：url----->%s" % url
        f = urllib2.urlopen(url)
        s = f.read()
        # 读取json数据
        j = json.loads(s)
        j.keys()

        if j.get("errcode", None):
            print (u"错误信息 >>> >>> %s" % j['errmsg']).encode('utf-8')
            return
        token = j['access_token']
        return token
# 开始推送

    def do_push(self, touser, template_id, url, data, topcolor):
        if topcolor.strip() == '':
            topcolor = "#7B68EE"
        dict_arr = {'touser': touser, 'template_id': template_id,
                    'url': url, 'topcolor': topcolor, 'data': data}
        json_template = json.dumps(dict_arr)
        token = self.getToken()

        if not token:
            return
        requst_url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=" + token
        content = self.post_data(requst_url, json_template)
        # 读取json数据
        j = json.loads(content)
        j.keys()
        errcode = j['errcode']
        errmsg = j['errmsg']
        return errmsg

# 模拟post请求
    def post_data(self, url, para_dct):
        para_data = para_dct
        f = urllib2.urlopen(url, para_data)
        content = f.read()
        return content

    def sendSms(self, uname, send_str, color='#173177'):
        #
        dt = {
            "data": {
                "value": u"zec:云币网-海枫藤=3",
                "color": u"#173177"
            }
        }

        dt["data"]["value"] = send_str
        dt["data"]["color"] = color
        self.do_push(wx_no_info[uname], wx_data_template, '', dt, '')

        return


# 微信号
wx_no_info = {'tq': 'oXRWit3M9MdVfN-bZWMTDmj967rg',
              'wh': 'oXRWit0yPlhz3wvuGeANPpk3HPeY',
              'zj': 'oXRWit3A7CsuaZzxcrTTmCqb7i_E',
              'tt': 'oXRWit9hAtbxjXPoL1xsqkzN0NFg',
              'lzj': 'oXRWitzuVn8IaniAHnBcsC9n9HAI',
              'gpc': 'oXRWitytNLTHGOZ92pUgA_Jj8xLM',
              'wm': 'oXRWit9ASFPGBZCfFwLTU2qZZJNc',
              }

# 微信数据模板
wx_data_template = 'wJNUcKu8nELKYyIJmy-pqI3F3GZW9OXOsmcO85fWftk'


#coins = ("zec","eth","etc")
coins = ("eth","etc")
users = ("tq",)

if __name__ == '__main__': 
    conf_path = os.path.split(os.path.realpath(__file__))[0] + "/conf/"
    
    thi = BanStart()
    coins_info = SosobtcUtil(0.05, 0.05).getCoinInfo(coins)
    # print "zec----->%.2f---->%s" % (coins_info['zec']['soso_offv'], coins_info['zec']['notify_str'])
    # print "eth----->%.2f---->%s" % (coins_info['eth']['soso_offv'], coins_info['eth']['notify_str'])
    
    tq_conf = ConfUtil(conf_path).getUserBanConf(users, coins)
    # print "---->%s" % (users_info['tq']['etc']['max_ban'])
    # print "---->%s" % (users_info['tq']['etc']['min_ban'])

    #
    yunUtil = YunUtil()
#搬砖
    for user in users:
        # 发送通知内容
        send_str = u""
        for coin in coins:
            print ">>> >>> %s --------------------" % coin
            # print "%s-------------->%s" % (coin, coins_info[coin]['notify_str'])
            # 搬砖状态
            ban_flag = -1
            #差价
            if tq_conf.has_key(user) and tq_conf[user].has_key(coin):
                # print u"%s----%s---->%s %s " % (user, coin, users_info[user][coin]['max_off'], users_info[user][coin]['min_off'])
                if tq_conf[user][coin]['notify'] == '1':
                    ban_flag = 0
                    yunbi = float(coins_info[coin]['yunbi'])
                    szzc = float(coins_info[coin]['szzc'])
                    soso_offv = float(coins_info[coin]['soso_offv'])
                    notify_str = coins_info[coin]['notify_str']
                    # ban差价
                    max_ban_str = tq_conf[user][coin]['max_ban']
                    min_ban_str = tq_conf[user][coin]['min_ban']
                    max_ban = 0.0
                    min_ban = 0.0
                    if max_ban_str != 'None' :
                        max_ban = float(max_ban_str)
                    if min_ban_str != 'None' :
                        min_ban = float(min_ban_str)
                    #每笔限量
                    max_volume = float(tq_conf[user][coin]['max_volume'])
                    min_volume = float(tq_conf[user][coin]['min_volume'])
                    
                    # print (u"%s差价:%s(soso_offv) | %s(notify_str) | %s(max_off) | %s(min_off)" % (coin, soso_offv, notify_str, max_ban_str, min_ban_str)).encode('utf-8')
                    # 差价
                    if min_ban_str != 'None' and soso_offv > min_ban:
                        ban_flag = 1  # yunbi buy and szzc sell
                        print u"soso --> %s差价:%s > %s 可能有的搬 yunbi buy and szzc sell " % (coin, notify_str, min_ban_str)
                    if max_ban_str != 'None' and soso_offv < max_ban:
                        ban_flag = 2    #szzc buy and yunbi sell
                        print u"soso --> %s差价:%s < %s 可能有的搬 szzc buy and yunbi sell " % (coin, notify_str, max_ban_str)
                    
                    #先判断是否有未处理的订单，有--》直接next
                    if ban_flag == 1 or ban_flag == 2 :   
                        yun_ord_num = yunUtil.getMyOrderCount(coin)
                        szzc_ord_num = szzcUtil.getMyOrderCount(coin)
                        if yun_ord_num < 1 and szzc_ord_num < 1 :
                            ban_flag = ban_flag + 2     # 3 or 4
                        else :
                            if yun_ord_num > 0 :
                                print u"yunbi %s 有未处理的订单，需要手动处理，或者等待订单匹配" % coin
                                if yun_ord_num > 100 :
                                    sms_str = u"warning>>> yunbi %s 有未处理的订单，超过%dminute" % (coin, yun_ord_num/60)
                                    print sms_str
                                    thi.sendSms(user, sms_str, '#FF0000')
                            if szzc_ord_num > 0 :
                                print u"szzc %s 有未处理的订单，需要手动处理，或者等待订单匹配" % coin
                                if szzc_ord_num > 100 :
                                    sms_str = u"warning>>> szzc %s 有未处理的订单，超过%dminute" % (coin, szzc_ord_num/60)
                                    print sms_str
                                    thi.sendSms(user, sms_str, '#FF0000')

                    #账户信息
                    yunbi_cny = 0.0
                    yunbi_coin = 0.0
                    szzc_cny = 0.0
                    szzc_coin = 0.0

                    #按最少搬砖量 判断账户条件 是否 满足
                    if ban_flag == 3:   #yunbi buy and szzc sell
                        yunbi_cny = yunUtil.getCurrency('cny')
                        if yunbi_cny > yunbi * min_volume :
                            # print u"yunbi --> 最小限量: %.2f(cny) >  %.2f(yunbi) * %.2f(min_volume) = %.2f  yunbi人民币满足" % (yunbi_cny, yunbi, min_volume, yunbi*min_volume)
                            szzc_coin = szzcUtil.get_balance(coin)
                            if szzc_coin > min_volume :
                                # print u"szzc --> 最小限量%s(数字币): %.2f > %.2f  szzc数字币数量满足" % (coin, szzc_coin, min_volume)
                                ban_flag = 5 
                            else :
                                print u"szzc --> 最小限量%s(数字币): %.2f > %.2f  szzc数字币数量【不满足】" % (coin, szzc_coin, min_volume)
                        else :
                            print u"yunbi --> 最小限量: %.2f(cny) >  %.2f(yunbi) * %.2f(min_volume) = %.2f  yunbi人民币【不满足】" % (yunbi_cny, yunbi, min_volume, yunbi*min_volume)

                    if ban_flag == 4:   # szzc buy and yunbi sell
                        szzc_cny = szzcUtil.get_balance('cny')
                        if szzc_cny > szzc * min_volume :
                            # print u"szzc --> 最小限量: %.2f(cny) >  %.2f(yunbi) * %.2f(min_volume) = %.2f  szzc人民币满足" % (szzc_cny, szzc, min_volume, szzc*min_volume)
                            yunbi_coin = yunUtil.getCurrency(coin)
                            if yunbi_coin > min_volume :
                                # print u"yunbi --> 最小限量%s(数字币): %.2f > %.2f  szzc数字币数量满足" % (coin, yunbi_coin, min_volume)
                                ban_flag = 6 
                            else :
                                print u"yunbi --> 最小限量%s(数字币): %.2f > %.2f  yunbi数字币数量【不满足】" % (coin, yunbi_coin, min_volume)
                        else :
                            print u"szzc --> 最小限量: %.2f(cny) >  %.2f(yunbi) * %.2f(min_volume) = %.2f  szzc人民币【不满足】" % (szzc_cny, szzc, min_volume, szzc*min_volume)

                    #可以搬的数量
                    ban_volume = 0.0

                    # 精确云币可搬价格
                    if ban_flag == 5:
                        # yunbi buy 就要看卖的量和价格   yunbi buy and szzc sell
                        yun_volume, yunbi = yunUtil.getMarketInfo('sell', coin, max_volume, min_volume)
                        szzc_volume, szzc = szzcUtil.getMarketInfo('buy', coin, max_volume, min_volume)
                        # print u"yunbi --> %s 市场【卖】数量:%.2f 价格:%.2f " % (coin, yun_volume, yunbi)
                        # print u"szzc --> %s 市场【买】数量:%.2f 价格:%.2f " % (coin, szzc_volume, szzc)
                        if szzc - yunbi > min_ban :
                            ban_volume = min(yun_volume, szzc_volume)
                            ban_flag = 7    # yunbi buy and szzc sell
                            print u"market --> %s差价:%.2f(szzc) - %.2f(yunbi) = %.2f > %s 市场价格满足 yunbi buy and szzc sell " % (coin, szzc, yunbi, szzc-yunbi, min_ban_str)
                        else :
                            print u"market --> %s差价:%.2f(szzc) - %.2f(yunbi) = %.2f > %s 市场价格【不满足】 yunbi buy and szzc sell " % (coin, szzc, yunbi, szzc-yunbi, min_ban_str)

                    if ban_flag == 6:
                        # yunbi sell 就要看卖的量和价格   szzc buy and yunbi sell
                        yun_volume, yunbi = yunUtil.getMarketInfo('buy', coin, max_volume, min_volume)
                        szzc_volume, szzc = szzcUtil.getMarketInfo('sell', coin, max_volume, min_volume)
                        # print u"yunbi --> %s 当前【买】数量:%.2f 价格:%.2f " % (coin, yun_volume, yunbi)
                        # print u"szzc --> %s 当前【卖】数量:%.2f 价格:%.2f " % (coin, szzc_volume, szzc)
                        if szzc - yunbi < max_ban :
                            ban_volume = min(yun_volume, szzc_volume)
                            ban_flag = 8    # szzc buy and yunbi sell
                            print u"market --> %s差价:%.2f(szzc) - %.2f(yunbi) = %.2f < %s 市场价格满足 szzc buy and yunbi sell " % (coin, szzc, yunbi, szzc-yunbi, max_ban_str)
                        else :
                            print u"market --> %s差价:%.2f(szzc) - %.2f(yunbi) = %.2f < %s 市场价格【不满足】 szzc buy and yunbi sell " % (coin, szzc, yunbi, szzc-yunbi, max_ban_str)

                    #（不用请求账户信息）根据市场的 ban_volume 再次判断判断账户条件 是否有足够的cny 和 coin
                    if ban_flag == 7 :   #yunbi buy and szzc sell
                        if yunbi_cny > yunbi * ban_volume :
                            # print u"yunbi --> 当前: %.2f(cny) >  %.2f(yunbi) * %.2f(ban_volume) = %.2f  yunbi人民币满足" % (yunbi_cny, yunbi, ban_volume, yunbi*ban_volume)
                            if szzc_coin > ban_volume :
                                # print u"szzc --> %s 数字币: %.2f > %.2f  szzc数字币数量满足" % (coin, szzc_coin, ban_volume)
                                ban_flag = 9 
                            else :
                                print u"szzc --> %s 数字币: %.2f > %.2f  szzc数字币数量【不满足】" % (coin, szzc_coin, ban_volume)
                        else :
                            print u"yunbi --> 当前: %.2f(cny) >  %.2f(yunbi) * %.2f(ban_volume) = %.2f  yunbi人民币【不满足】" % (yunbi_cny, yunbi, ban_volume, yunbi*ban_volume)

                    if ban_flag == 8 :   # szzc buy and yunbi sell
                        if szzc_cny > szzc * ban_volume :
                            # print u"szzc --> 当前: %.2f(cny) >  %.2f(yunbi) * %.2f(ban_volume) = %.2f  szzc人民币满足" % (szzc_cny, szzc, ban_volume, szzc*ban_volume)
                            if yunbi_coin > ban_volume :
                                # print u"yunbi --> %s 数字币: %.2f > %.2f  szzc数字币数量满足" % (coin, yunbi_coin, ban_volume)
                                ban_flag = 10 
                            else :
                                print u"yunbi --> %s 数字币: %.2f > %.2f  szzc数字币数量【不满足】" % (coin, yunbi_coin, ban_volume)
                        else :
                            print u"szzc --> 当前: %.2f(cny) >  %.2f(yunbi) * %.2f(ban_volume) = %.2f  szzc人民币【不满足】" % (szzc_cny, szzc, ban_volume, szzc*ban_volume)

                    #限制小数点位数，szzc --> ERR_QUANTITY_DECIMALS
                    ban_volume = round(ban_volume, 2)

                    #创建订单
                    if ban_flag == 9 :   # yunbi buy and szzc sell
                        sms_str = u"yunbi %.2f(price) buy %.2f(volume) and szzc %.2f(price) sell %.2f(volume)" % (yunbi, ban_volume, szzc, ban_volume)
                        szzc_order_id = szzcUtil.create_order(coin, 'sell', float(szzc), ban_volume)
                        if szzc_order_id > 0 : 
                            yunbi_order_id = yunUtil.createOrder(coin, 'buy', float(yunbi), ban_volume)
                            if yunbi_order_id > 0 :
                                ban_flag = 200
                                sms_str = u"%s 订单创建成功! %s" % (coin, sms_str)
                                print sms_str
                                thi.sendSms(user, sms_str, '#009900')
                            else :
                                print u"yunbi --> %s 订单创建失败 ... %s" % (coin, sms_str)
                        else :
                            print u"szzc --> %s 订单创建失败 ... %s" % (coin, sms_str)
                            
                    if ban_flag == 10 :   # szzc buy and yunbi sell
                        sms_str = u"szzc %.2f(price) buy %.2f(volume) and yunbi %.2f(price) sell %.2f(volume)" % ( szzc, ban_volume, yunbi, ban_volume)
                        szzc_order_id = szzcUtil.create_order(coin, 'buy', float(szzc), float(ban_volume))
                        if szzc_order_id > 0 : 
                            yunbi_order_id = yunUtil.createOrder(coin, 'sell', float(yunbi), float(ban_volume))
                            if yunbi_order_id > 0 :
                                ban_flag = 200
                                sms_str =  u"%s 订单创建成功! %s" % (coin, sms_str)
                                print sms_str
                                thi.sendSms(user, sms_str, '#009900')
                            else :
                                print u"yunbi --> %s 订单创建失败 ... %s" % (coin, sms_str)
                        else :
                            print u"szzc --> %s 订单创建失败 ... %s" % (coin, sms_str)

            print "-------------------- %s >>> >>> %d \r\n" % (coin, ban_flag)


