#-*- coding: UTF-8 -*-
import time
import datetime


def utc2local(utc_st):
    """UTC时间转本地时间（+8:00）"""
    now_stamp = time.time()
    local_time = datetime.datetime.fromtimestamp(now_stamp)
    utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
    offset = local_time - utc_time
    local_st = utc_st + offset
    return local_st

def local2utc(local_st):
    """本地时间转UTC时间（-8:00）"""
    time_struct = time.mktime(local_st.timetuple())
    utc_st = datetime.datetime.utcfromtimestamp(time_struct)
    return utc_st

GMT_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

def utc_str2local(utc_str):
    # print 'utc_str2local--->begin'
    utc_tm = datetime.datetime.strptime(utc_str, GMT_FORMAT)
    return utc2local(utc_tm)
    
#传入格林市时间，返回与当前时间差    
def get_off_by_utc_str(utc_str):
    # print '--->'+utc_str
    local_tm = utc_str2local(utc_str)
    # print local_tm
    now_tm = datetime.datetime.fromtimestamp(time.time())
    return (now_tm - local_tm).seconds




# utc_time = datetime.datetime(2014, 9, 18, 10, 42, 16, 126000)
# print type(utc_time)

# # utc转本地
# local_time = utc2local(utc_time)
# print local_time.strftime("%Y-%m-%d %H:%M:%S")
# # output：2014-09-18 18:42:16


# # 本地转utc
# utc_tran = local2utc(local_time)
# print utc_tran.strftime("%Y-%m-%d %H:%M:%S")
# # output：2014-09-18 10:42:16



# tm_str = u'2017-07-17T03:26:54Z'
# # utc_tm = utc_str2local(tm_str)
# # now_tm = datetime.datetime.fromtimestamp(time.time())
# # off_tm = now_tm - utc_tm
# # print type(off_tm)
# # print off_tm
# # print off_tm.seconds

# print get_off_by_utc_str(tm_str)