#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
import json
import time
import os

from sosobtcUtil import SosobtcUtil
from confUtil import ConfUtil
from fileReadUtil import FileReadUtil


class WxStart(object):

    def __init__(self, appid, secrect):
        self.appid = appid
        self.secrect = secrect
# 获取accessToken

    def getToken(self):
        # 判断缓存
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + \
            self.appid + "&secret=" + self.secrect
        print "getToken：url----->%s" % url
        f = urllib2.urlopen(url)
        s = f.read()
        # 读取json数据
        j = json.loads(s)
        j.keys()

        if j.get("errcode", None):
            print u"错误信息 >>> >>> %s" % j['errmsg']
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

    def sendSms(self, uname, data):
        # tq
        thi.do_push(wx_no_info[uname], wx_data_template, '', data, '')

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
#
dt = {
    "data": {
        "value": u"zec:云币网-海枫藤=3",
        "color": "#173177"
    }
}

#
coins = ("zec", "eth", "etc", "etp", "btc", "bts")
users = ("tq","zj","tt","lzj","gpc","wm")


thi = WxStart('wx5d2607e7bf434326', '6a005490e16bae05e256e06ebf3118db')
coins_info = SosobtcUtil(0.05, 0.05).getCoinInfo(coins)
print "zec----->%.2f---->%s" % (coins_info['zec']['soso_offv'], coins_info['zec']['notify_str'])
print "eth----->%.2f---->%s" % (coins_info['eth']['soso_offv'], coins_info['eth']['notify_str'])

conf_path = os.path.split(os.path.realpath(__file__))[0] + "/"
users_info = ConfUtil(conf_path).getUserConf(users, coins)
# print "---->%s" % (users_info['tq']['zec']['logic'])

for user in users:
    # 是否发送通知
    send_flag = 0
    # 发送通知内容
    send_str = u""
    for coin in coins:
        # print "%s-------------->%s" % (coin, coins_info[coin]['notify_str'])
        #差价
        if users_info.has_key(user) and users_info[user].has_key(coin):
            # print u"%s----%s---->%s %s " % (user, coin, users_info[user][coin]['max_off'], users_info[user][coin]['min_off'])
            if users_info[user][coin]['notify'] == '1':
                yunbi = float(coins_info[coin]['yunbi'])
                szzc = float(coins_info[coin]['szzc'])
                soso_offv = float(coins_info[coin]['soso_offv'])
                notify_str = coins_info[coin]['notify_str']
                # 差价
                max_off_str = users_info[user][coin]['max_off']
                min_off_str = users_info[user][coin]['min_off']
                max_off = 0.0
                min_off = 0.0
                if max_off_str != 'None' :
                    max_off = float(max_off_str)
                if min_off_str != 'None' :
                    min_off = float(min_off_str)
                # 市价
                max_val_str = users_info[user][coin]['max_val']
                min_val_str = users_info[user][coin]['min_val']
                max_val = 0.0
                min_val = 0.0
                if max_val_str != 'None' :
                    max_val = float(max_val_str)
                if min_val_str != 'None' :
                    min_val = float(min_val_str)

                # print (u"%s差价:%s(soso_offv) | %s(notify_str) | %s(max_off) | %s(min_off)" % (coin, soso_offv, notify_str, max_off_str, min_off_str)).encode('utf-8')
                # print (u"%s市价:%s(yunbi) | %s(szzc) | %s(max_val) | %s(min_val)" % (coin, yunbi, szzc, max_val_str, min_val_str)).encode('utf-8')
                # 差价
                if min_off_str != 'None' and soso_offv > min_off:
                    send_flag = 1
                    send_str = u"%s差价:%s > %s\r\n" % (send_str, notify_str, min_off_str)
                if max_off_str != 'None' and soso_offv < max_off:
                    send_flag = 1
                    send_str = u"%s差价:%s < %s\r\n" % (send_str, notify_str, max_off_str)
                #市价
                if min_val > 0 :
                    if  yunbi > min_val :
                        send_flag = 1
                        send_str =  u"%s%s市价:yunbi:%s > %s\r\n" % (send_str, coin, str(yunbi), min_val_str)
                    if  szzc > min_val :
                        send_flag = 1
                        send_str = u"%s%s市价:szzc:%s > %s\r\n" % (send_str, coin, str(szzc), min_val_str)

                if max_val > 0 :
                    if yunbi > 0 and yunbi < max_val :
                        send_flag = 1
                        send_str = u"%s%s市价:yunbi:%s < %s\r\n" % (send_str, coin, str(yunbi), max_val_str)
                    if szzc > 0 and szzc < max_val :
                        send_flag = 1
                        send_str = u"%s%s市价:szzc:%s < %s\r\n" % (send_str, coin, str(szzc), max_val_str)

    # 微信通知
    # print u"000---->%s " % send_flag
    if send_flag == 1:
        print (u"满足价格要求,通知%s---->%s" % (user, send_str)).encode('utf-8')
        dt["data"]["value"] = send_str
        thi.sendSms(user, dt)


# if not off :
#     print u"价格不符合要求，退出！"
# else :
#     #价格符合通知要求，进一步判断是否要微信通知
#     f = FileReadUtil("/Users/app/Documents/zcash/porter/last_wx_send_record.txt", 1000, 0.5*60*60)
#     flag = f.needSms()
#     f._file.close()
#     #print "flag------->", flag
#     if flag :
#         #微信通知
#         dt["data"]["value"]=off
#         s.sendSms(dt)
