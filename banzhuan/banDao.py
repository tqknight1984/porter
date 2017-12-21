#coding=utf-8

import sqlite3,sys,os


reload(sys)
sys.setdefaultencoding('utf-8')


DB_TICKER = 'test.db'
DB_WALLET = 'wallet.db'

class banDao(object):
    
    @staticmethod
    def createTab():
        if os.path.isfile(DB_TICKER) :
            os.remove(DB_TICKER)
        
        conn = sqlite3.connect(DB_TICKER)
        print "Opened database successfully";

        # conn.execute('''CREATE TABLE if not exists COMPANY
        #         (ID INT PRIMARY KEY     NOT NULL,
        #         NAME           TEXT    NOT NULL,
        #         AGE            INT     NOT NULL,
        #         ADDRESS        CHAR(50),
        #         SALARY         REAL);''')

        conn.execute('''CREATE TABLE if not exists ticker
                (id     INT PRIMARY KEY     NOT NULL,
                plat            CHAR(50)    NOT NULL,
                up_tm           INT         NOT NULL,
                coin            CHAR(50)    NOT NULL,
                market            CHAR(50)    NOT NULL,
                bid            REAL    NOT NULL,
                ask            REAL    NOT NULL,
                last            REAL    NOT NULL,
                zzz          REAL);      
                ''')

        print "Table created successfully";

        conn.close()
        
    @staticmethod
    def insertTicker(id, plat, up_tm, coin ,market, bid, ask, last) :
        conn = sqlite3.connect(DB_TICKER)
        print "Opened database successfully";
        conn.execute("DELETE from ticker where plat='%s' and market='%s';" % (plat, market))
        ist_sql = '''INSERT INTO ticker 
            (id, plat, up_tm, coin ,market, bid, ask, last) 
            VALUES 
            (%s,'%s', %s, '%s' ,'%s','%s' , '%s', '%s' );''' % (id, plat, up_tm, coin ,market, bid, ask, last )
        print '-ist_sql-------------', ist_sql
        conn.execute(ist_sql )
        conn.commit()
        conn.close()
        
    @staticmethod
    def selectTicker( plat,  market) :
        conn = sqlite3.connect(DB_TICKER)
        print "Opened database successfully";
        
        sel_sql = "SELECT id, plat, market, up_tm  from ticker where plat='%s' and market='%s';" % (plat, market)
        # print '-sel_sql-------------', sel_sql

        cursor = conn.execute(sel_sql)
        for row in cursor :
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
    def selectPlat( plat) :
        conn = sqlite3.connect(DB_TICKER)
        sel_sql = "SELECT id, plat, market, bid, ask, last  from ticker where plat='%s';" % (plat)
        # print '-sel_sql-------------', sel_sql
        cursor = conn.execute(sel_sql)
        for row in cursor :
            print 'row ======>', row[0], row[1], row[2], row[3], row[4], row[5]
        conn.close()


    if __name__  ==  "__main__":
        print u"中文"

