# -*- coding:utf-8 -*-                                                                         
import requests, time, pymysql, urllib
import pandas as pd
from datetime import datetime,timedelta
from urllib.parse import quote

if __name__ == '__main__':
    ts_lasthour = datetime.utcnow().replace(minute=0,second=0,microsecond=0)-timedelta(hours=1)
    conn = pymysql.connect(host='127.0.0.1',user='root',passwd='qwer1234',db='scrapy',charset='utf8mb4')
    cur = conn.cursor()

# get subscribed word
    cur.execute('SELECT word,user,sckey FROM word_subscribe WHERE enable=1')
    dt_word = cur.fetchall()
    dt_word = pd.DataFrame(list(dt_word),columns=['word','user','sckey'])

# get items
    ts_str = ts_lasthour.strftime('%Y-%m-%d %H:%M:%S')
    cur.execute("SELECT title,url,webname FROM secondHand WHERE date_format(time,'%%Y-%%m-%%d %%H:00:00')=%s",ts_str)
    dt_items = cur.fetchall()
    dt_items = pd.DataFrame(list(dt_items),columns=['title','url','webname'])
    dt_items['title'] = dt_items['title'].str.replace('&','')
    dt_items['url'] = dt_items['url'].str.replace('&','')
    dt_items['mkd'] = "["+dt_items['title']+"]"+"("+dt_items['url']+")  \n"

# filter items
    for i in range(len(dt_word)):
        w = dt_word['word'][i]
        k = dt_word['sckey'][i]
        idx = dt_items['title'].str.contains(w,case=False)
        if any(idx)==True:
            cur.execute("UPDATE word_subscribe SET counts=counts+%s WHERE word=%s and sckey=%s",(sum(idx),w,k))
            cur.connection.commit()
            content = dt_items['mkd'][idx].str.cat()
            url = 'https://sc.ftqq.com/'+dt_word['sckey'][i]+'.send?'+'text='+w+'&desp='+content
            rtn = urllib.request.urlopen(quote(url,safe=":?=/&"))
            print("[%s] User:%s\t\tWord:%s\t\tCount:%d" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'),dt_word['user'][i],w,sum(idx)))
