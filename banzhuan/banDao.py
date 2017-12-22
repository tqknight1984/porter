# coding=utf-8

import sqlite3
import sys
import os


reload(sys)
sys.setdefaultencoding('utf-8')


DB_TICKER = 'ticker.db'
DB_ACCOUNT = 'account.db'
DB_MY_ORDER = 'my_order.db'


class banDao(object):

    @staticmethod
    def createTicker():
        if os.path.isfile(DB_TICKER):
            os.remove(DB_TICKER)

        conn = sqlite3.connect(DB_TICKER)
        # ticker    id     INT PRIMARY KEY     NOT NULL,
        conn.execute('''CREATE TABLE if not exists tb_ticker
                (
                plat            CHAR(50)    NOT NULL,
                up_tm           INT         NOT NULL,
                coin            CHAR(50)    NOT NULL,
                market          CHAR(50)    NOT NULL,
                bid            REAL    NOT NULL,
                ask            REAL    NOT NULL,
                last            REAL    NOT NULL,
                zzz          REAL);      
                ''')
        conn.close()

    @staticmethod
    def createAccount():
        if os.path.isfile(DB_ACCOUNT):
            os.remove(DB_ACCOUNT)

        conn = sqlite3.connect(DB_ACCOUNT)
        # account        id     INT PRIMARY KEY     NOT NULL,
        conn.execute('''CREATE TABLE if not exists tb_account
                (
                plat            CHAR(50)    NOT NULL,
                up_tm           INT         NOT NULL,
                coin            CHAR(50)    NOT NULL,
                balance          REAL      NOT NULL);      
                ''')
        conn.close()

    @staticmethod
    def insertTicker(plat, up_tm, coin, market, bid, ask, last):
        conn = sqlite3.connect(DB_TICKER)
        print "Opened database successfully"
        conn.execute(
            "DELETE from tb_ticker where plat='%s' and market='%s';" % (plat, market))
        ist_sql = '''INSERT INTO tb_ticker 
            ( plat, up_tm, coin ,market, bid, ask, last) 
            VALUES 
            ('%s', %s, '%s' ,'%s','%s' , '%s', '%s' );''' % ( plat, up_tm, coin, market, bid, ask, last)
        print '-ist_sql-------------', ist_sql
        conn.execute(ist_sql)
        conn.commit()
        conn.close()

    @staticmethod
    def insertAccount(plat, up_tm, account_ls):
        conn = sqlite3.connect(DB_ACCOUNT)
        for inf in account_ls :
            coin = inf['coin']
            balance = inf['balance']
            conn.execute(
                "DELETE from tb_account where plat='%s' and coin='%s';" % (plat, coin))
            ist_sql = '''INSERT INTO tb_account (plat, up_tm, coin ,balance) 
                VALUES 
                ('%s', %s, '%s' ,'%s' );''' % (plat, up_tm, coin, balance)
            print '-ist_sql-------------', ist_sql
            conn.execute(ist_sql)
        conn.commit()
        conn.close()

    @staticmethod
    def createMyOrder():
        if os.path.isfile(DB_MY_ORDER):
            os.remove(DB_MY_ORDER)

        conn = sqlite3.connect(DB_MY_ORDER)
        conn.execute('''CREATE TABLE if not exists tb_my_order
                (
                plat            CHAR(50)    NOT NULL,
                up_tm           INT         NOT NULL,
                coin            CHAR(50)    NOT NULL,
                market            CHAR(50)    NOT NULL,
                side            CHAR(50)    NOT NULL,
                price          REAL      NOT NULL,
                amount          REAL      NOT NULL);      
                ''')
        conn.close()

#  [{'status': u'ACTIVE', 'price': 9, 'amount': 10, 'coin': u'EOS', 'side': 'buy', 'market': u'tEOSUSD'}]
    @staticmethod
    def insertMyOrder(plat, up_tm, oderLs):
        conn = sqlite3.connect(DB_MY_ORDER)
        conn.execute("DELETE from tb_my_order where plat='%s';" % (plat))
        for odrDic in oderLs:
            coin = odrDic['coin']
            market = odrDic['market']
            side = odrDic['side']
            amount = odrDic['amount']
            price = odrDic['price']
            ist_sql = '''INSERT INTO tb_my_order (plat, up_tm, coin ,market, side, price, amount) 
                VALUES 
                ('%s', %s, '%s' ,'%s', '%s', '%s' ,'%s' );''' % (plat, up_tm, coin, market, side, price, amount)
            print '-ist_sql-------------', ist_sql
            conn.execute(ist_sql)
        conn.commit()
        conn.close()

    @staticmethod
    def selectMyOrder(plat):
        conn = sqlite3.connect(DB_MY_ORDER)
        sel_sql = "SELECT  plat, coin, market, side, price, amount from tb_my_order where plat='%s';" % (
            plat)
        # print '-sel_sql-------------', sel_sql
        cursor = conn.execute(sel_sql)
        for row in cursor:
            print 'row ======>', row[0], row[1], row[2], row[3], row[4], row[5]
        conn.close()


    @staticmethod
    def selectTicker(plat,  market):
        conn = sqlite3.connect(DB_TICKER)
        print "Opened database successfully"

        sel_sql = "SELECT id, plat, market, up_tm  from tb_ticker where plat='%s' and market='%s';" % (
            plat, market)
        # print '-sel_sql-------------', sel_sql

        cursor = conn.execute(sel_sql)
        for row in cursor:
            print '-zzz-------------'
            print "ID = ", row[0]
            print "plat = ", row[1]
            print "market = ", row[2]
            print "up_tm = ", row[3]

        # sql_cur = conn.cursor()
        # sql_cur.execute(sel_sql)
        # rows = sql_cur.fetchall()
        # for row in rows:
        #     print '-zzz-------------'
        #     print "ID = ", row[0]
        #     print "plat = ", row[1]
        #     print "market = ", row[2]
        #     print "up_tm = ", row[3]
        # sql_cur.close()
        conn.close()

    @staticmethod
    def selectTickers(plat):
        conn = sqlite3.connect(DB_TICKER)
        sel_sql = "SELECT plat, market, bid, ask, last  from tb_ticker where plat='%s';" % (
            plat)
        # print '-sel_sql-------------', sel_sql
        cursor = conn.execute(sel_sql)
        for row in cursor:
            print 'row ======>', row[0], row[1], row[2], row[3], row[4]
        conn.close()


    @staticmethod
    def selectCount(coin):
        conn = sqlite3.connect(DB_ACCOUNT)
        sel_sql = "SELECT  plat, balance from tb_account where coin='%s';" % (
            coin)
        # print '-sel_sql-------------', sel_sql
        cursor = conn.execute(sel_sql)
        for row in cursor:
            print 'row ======>', row[0], float(row[1])
        conn.close()



    if __name__ == "__main__":
        print u"中文"
