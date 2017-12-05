#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
import json
import time


class FileReadUtil(object):

    def __init__(self, fileName, lineLimit=5, offTm=3600):
        # print "__init__"
        self._fileName = fileName
        fo = open(fileName, "r")
        self._file = fo
        self._lineLimit = lineLimit
        self._offTm = offTm
        return

    def fileTest(self):
        print "------>", self._file.tell()

        return

    def hasLine(self, num):
        for index in range(num):
            line = self._file.next()
            print "line---%d--->%s --> %d" % (index, line, len(line))

        return False

    def lencount(self):
        return len(self._file.readlines())

    def firstLine(self):
        self._file.seek(0, 0)
        return self._file.readline()

    # 1：文件行数少于指定行数，追加行数并发送通知
    # 2：行数达到指定行数，且与第一行时间间隔在1小时以内，不操作文件，不发送通知
    # 3：达到指定行数，与第一行时间时间间隔超过1小时，重新开始写文件，并发送通知
    def getflag(self):
        line = self.lencount()
        if line < self._lineLimit:
            return 1
        else:
            off_tm = int(time.time()) - int(self.firstLine()[0:10])
            print "off_tm = ", off_tm
            if off_tm < self._offTm:
                return 2
        return 3

    def writeAdd(self):
        fo = open(self._fileName, "a")
        self._file = fo
        self._file.write(str(time.time()) + "\n")

        return

    def writeOver(self):
        fo = open(self._fileName, "w")
        self._file = fo
        self._file = fo
        self._file.write(str(time.time()) + "\n")
        return

    def needSms(self):
        flag = self.getflag()
        # print "flag------->", flag
        # 追加并发消息
        if flag == 1:
            print ">>> >>> 通知限制以内，追加并发消息"
            self.writeAdd()
            return True

        # 不发消息，不操作文件
        if flag == 2:
            print ">>> >>> 达到通知上限，不发消息，不操作文件"
            return False

        # 重写并发消息
        if flag == 3:
            print ">>> >>> 重置通知标识，重写并发消息"
            self.writeOver()
            return True


# print time.time()

# s = FileReadUtil("zzz.txt", 6, 3600)
# s.needSms()
# s._file.close()

# print time.time()
