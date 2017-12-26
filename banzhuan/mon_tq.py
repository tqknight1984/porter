#coding=utf-8
import httplib
import urllib
import os
import sys
import time
import datetime
import getopt
import smtplib
import json
import md5
import urlparse
import subprocess

from banDao import banDao
from zb_api import zb_api
from bfx_api import bfx_api

reload(sys)
sys.setdefaultencoding('utf-8')

phone_list = {
    'serv_warn' : [('18501735859', u'田')],
    'redis_warn' : [('18501735859', u'田')],
}

sms_url = '61.130.7.220:8023/MWGate/wmgw.asmx/MongateSendSubmit?userId=J50865&password=586536&' #pszMobis=" + phone  + "&pszMsg=" + e_msg + "&iMobiCount=1
hfile = None

email_flag = False
daily_flag = False

monpath = ""
http_path = '/data/app/nginx/html'
html_name = ""



html_txt = {
        'version' : '2.0.0',
        'ver':time.strftime("%Y%m%d%H%M%S", time.localtime()),
        'serv_warn' : 0,
        'redis_warn' : 0,
        'auto_warn' : 0,
        'depth_warn' : 0,
        'lastnews_warn' : 0,
        'pic_warn' : 0,
        'tousu_warn' : 0,
        'inf_warn' : 0,
        'bigshow_warn' : 0,
        'check_tm' : time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        'servers' : [],
        'redisInfo' : [],
        'spider' : [],

        'vs_name':'ZB vs BFX',
        'platform': ['zb', 'bfx'],
        'markets': ['btc_usdt','eos_usdt', 'eos_btc', 'eth_usdt', 'eth_btc', 'etc_usdt', 'etc_btc',  'xrp_usdt', 'xrp_btc','qtum_usdt', 'qtum_btc',],
        # 
        'myorders':[],
        'ticker_dic':{},
        'account_dic':{},
        'off_dic':{},
        
    }

#
def sendSMS(catalog,desc):
    
    sms_boo = True
    if os.path.isfile("sms.log") :
        with open("sms.log","r") as f: 
            tm = 0
            ln =  f.readline()
            if ln :
                tm = int(ln)
                print "f.readline()----->", tm
                off_tm = int(time.time()) - tm
                print "off_tm----->", off_tm

                if off_tm < (30 * 60 ) :
                    sms_boo = False
            f.close()

    print "sms_boo----->", sms_boo

    if sms_boo :
        
        with open("sms.log","w") as f :
            f.write(str( int(time.time()) ))
            f.close()

        for ph,name in phone_list[catalog]:
            kk = u'系统(' + desc + ')有异常，详细查看http://115.159.66.252/moni/che.html'
            msg = sms_url + "&pszMobis=" + ph  + "&pszMsg=" + urllib.urlencode({'message': kk.encode('utf8')}) + "&iMobiCount=1"
            getHttpStatus(msg,'',False)


def gen_html():
    from jinja2 import Environment,FileSystemLoader
    PATH = os.path.dirname(os.path.abspath(__file__))
    TEMPLATE_ENVIRONMENT = Environment(
        autoescape=False,
        loader=FileSystemLoader(os.path.join(PATH, monpath)),
        trim_blocks=False)
    def render_template(template_filename, context):
        return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)
    with open(html_name, 'w') as f:
        html = render_template('mon_tq.html', html_txt)
        f.write(html)
    subprocess.call("cp -rf " + html_name + " " + http_path + "/tianqin.html", shell=True);
    subprocess.call("rm -rf " + html_name, shell=True);


        
if __name__ == "__main__":
    
    monpath = os.path.dirname(sys.argv[0])
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ed", ["email","daily"])
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)

    for o, a in opts:
        if o == '-e':
            email_flag = True
        elif o == '-d':
            daily_flag = True
        elif o in ('-p','--path'):
            xls_path = a
        else:
            assert False, "unhandled option"

    print 'check_tm------->',html_txt['check_tm']
    html_name = http_path + time.strftime("/tianqin_%Y%m%d%H.html", time.localtime())
    print 'html_name------->',html_name

    zb = zb_api()
    bfx = bfx_api()

    ticker_dic = {}

    #myOrder
    # myorders = banDao.selectMyOrderByAll()
    #bfx未完成的挂单
    myorders = bfx.get_act_orders()
    zb_odr_ls = zb.getOrdersNew()
    for odr in zb_odr_ls :
        myorders.append(odr)
    print u'bfx未完成的挂单------->',myorders

    #账户信息
    account_dic = {}
     #bfx
    bfx_balance_ls = bfx.get_balance()
    for bfx_balance in bfx_balance_ls :
        # print 'coin---bfx---->', bfx_balance['type'] ,bfx_balance['currency'] ,bfx_balance['available'] 
        account_dic['bfx_'+bfx_balance['currency']] = bfx_balance['available'] 
    #zb    
    zb_acc_ls = zb.get_account_info()
    for zb_acc in zb_acc_ls :
        # print 'coin---zb---->', zb_acc['coin'] ,zb_acc['balance'] 
        coin = zb_acc['coin'].lower()
        account_dic['zb_'+coin] = zb_acc['balance'] 

    print '---->', account_dic


    for plat in html_txt['platform'] :
        for market in html_txt['markets'] :
            db_market = market.replace('_', '/')
            
            zb_symb = market
            bfx_symb = market.replace('_','')
            bfx_symb = 't'+ (bfx_symb.replace('usdt','usd').upper())
            bfx_symb = bfx_symb.replace('QTUM','QTM')
            print 'zb_symb------->', zb_symb
            print 'bfx_symb------->', bfx_symb
            

            # #ticker
            # zb_trick = zb.getZbTicker(zb_symb)
            # bfx_trick = bfx.get_symb_tick(bfx_symb)
            # time.sleep(1)

            # #ticker from DB
            zb_trick = banDao.selectTicker('zb', db_market)
            bfx_trick = banDao.selectTicker('bfx', db_market)

            ticker_dic['zb_'+market] = zb_trick
            ticker_dic['bfx_'+market] = bfx_trick

            #未完成的挂单
            # zb_odr = zb.get_oders(zb_symb)
            # for odr in zb_odr :
            #     myorders.append(odr)
                
    print "myorders-------------->",myorders
    print "ticker_dic-------------->",ticker_dic
    print "account_dic-------------->",json.dumps(account_dic)

    html_txt['myorders'] = myorders
    html_txt['ticker_dic'] = ticker_dic
    html_txt['account_dic'] = json.dumps(account_dic)

    #差价 百分比
    off_dic = {}
    plat1 = html_txt['platform'][0]
    plat2 = html_txt['platform'][1]
    for mkt in html_txt['markets'] :
        p1v = ticker_dic[plat1+'_'+mkt]
        p2v = ticker_dic[plat2+'_'+mkt]

        p1v1 = p1v[0]
        p1v2 = p1v[1]
        p2v1 = p2v[0]
        p2v2 = p2v[1]

        pot = 0;
        v_str = str(p1v1)
        if len(str(p1v1)) <= len(str(p2v1)) :
            v_str = str(p1v1)
        else :
            v_str = str(p2v1)
        start = v_str.index(".");
        if start != -1 :
            pot = len(v_str[start+1:])
        # print "p1v1-------------->",p1v1
        # print "p2v1-------------->",p2v1
        # print "pot-------------->",pot

        #zb --> bfx      zb卖bfx买
        off1 = float(p1v2 - p2v1)
        avg1 = (p1v2 + p2v1)/2
        perc1 = '%.2f' % ( 100 * off1 / avg1)

        # print "off1-------------->",off1
        # print "perc1-------------->",perc1
        
        off_dic[mkt+'_off1'] = round(off1, pot)
        off_dic[mkt+'_perc1'] = perc1

        #bfx --> zb      bfx卖zb买
        off2 = float(p1v1 - p2v2)
        avg2 = (p2v2 + p1v1)/2
        perc2 = '%.2f' % ( 100 * off2 / avg2)

        # print "off2-------------->",off2
        # print "perc2-------------->",perc2
        
        off_dic[mkt+'_off2'] = round(off2, pot)
        off_dic[mkt+'_perc2'] = perc2
        
    html_txt['off_dic'] = off_dic



    # if (os.path.exists(html_name)):
    #     os.remove(html_name)

    gen_html()

    # if (html_txt["serv_warn"] > 0):
    #     sendSMS("serv_warn","服务器指标")

# #爬虫
#     for srs in html_txt['spider'] :
#         print srs.get("name","------"), srs.get("errcount","---")
#         if "最新资讯发布时间" != srs['name'] and srs.get("errcount",0) > 0 :
#             sendSMS("serv_warn","%s爬虫指标异常" % srs.get("name","爬虫"))
    
