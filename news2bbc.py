#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import datetime
import urllib2
import json
from bs4 import BeautifulSoup  


def getHtml(url):
    
    resp = urllib2.urlopen(url).read()
    # print resp
    soup = BeautifulSoup(resp)
    # print soup.prettify()

    # top = soup.select('.news-details-top')
    # print type(top[0].h1)

    title = soup.select('.news-details-top h1')[0].string
    title = title.replace('&nbsp', ' ')
    # print title

    adddate = soup.select('.author-info span')[0].select('a')[0].string
    # print adddate
    source = soup.select('.author-info span')[1].select('a')[0]['href']
    # print source
    editor = soup.select('.author-info span')[2].select('a')[0].string
    # print editor
    keyword = soup.select('head meta[name="keywords"]')[0]['content']
    # print keyword
    catalog = ''
    guides = soup.select('.breadcrumb-nav p a')
    # print guides
    for cata in guides :
        print unicode(cata.string)
        if unicode(cata.string) == u'正文' :
            break
        else :
            catalog = unicode(cata.string)
    print catalog
    


     



if __name__ == '__main__':
    print "---"
    url = 'http://inf.315che.com/n/2017_08/854640/'


    getHtml(url)




       