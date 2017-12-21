##coding=utf-8

import sqlite3,sys,os,time
from banDao import banDao


reload(sys)
sys.setdefaultencoding('utf-8')

class start():
   

    if __name__  ==  "__main__":

        proj_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        

        print u"-------->",proj_path
        banDao.createTicker()
        for i in range(1) :
            banDao.insertTicker(i,'zb', time.time(), 'btc', 'btc/usdt', '1111', '2222', '33333')    
            banDao.selectTicker('zb', 'btc/usdt')  




