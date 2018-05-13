# *-* coding:utf8 *-*
from datetime import datetime,timedelta
import os

ts = datetime.strptime('2018-04-15 11:00:00','%Y-%m-%d %H:%M:%S')
ts_now = datetime.strptime('2018-05-12 23:00:00','%Y-%m-%d %H:%M:%S')

while(ts<ts_now):
    cmd = 'python word_count.py %s' %(ts.strftime('%Y-%m-%dT%H:%M:%S'))
    os.system(cmd)
    print('time:%s\tcmd:%s' %(ts,cmd))
    ts = ts + timedelta(hours=1)
