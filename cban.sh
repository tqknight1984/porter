for pid in `ps -ef|grep collect_job.py|grep -v grep |awk '{print $2}'`
do
        kill -9 $pid
done
