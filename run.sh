#!/bin/sh
#source /etc/profile
#export PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/root/bin:/data/app/jdk764/bin:/data/app/zookeeper-3.4.8/bin:/data/app/zookeeper-3.4.8/conf
cd /usr/local/bin/
/usr/local/bin/python /data/app/che_py/porter/wxStart.py








* * * * * /usr/bin/python /data/app/tq/zb/zb.py
* * * * * sleep 20;/usr/bin/python /data/app/tq/zb/zb.py
* * * * * sleep 40;/usr/bin/python /data/app/tq/zb/zb.py

* * * * * /usr/bin/python /data/app/tq/bfx/bfx.py
* * * * * sleep 20;/usr/bin/python /data/app/tq/bfx/bfx.py
* * * * * sleep 40;/usr/bin/python /data/app/tq/bfx/bfx.py

* * * * * /usr/bin/python /data/app/tq/moni/mon_sys.py
* * * * * sleep 30; /usr/bin/python /data/app/tq/moni/mon_sys.py