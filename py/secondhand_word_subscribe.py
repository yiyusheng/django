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
    unique_key = dt_word['sckey'].unique()

# get items
    ts_str = ts_lasthour.strftime('%Y-%m-%d %H:%M:%S')
    cur.execute("SELECT title,url,webname FROM secondHand WHERE date_format(create_time,'%%Y-%%m-%%d %%H:00:00')=%s ORDER BY create_time DESC",ts_str)
    dt_items = cur.fetchall()
    dt_items = pd.DataFrame(list(dt_items),columns=['title','url','webname'])
    dt_items['title'] = dt_items['title'].str.replace('&','')
    dt_items['url'] = dt_items['url'].str.replace('&','')
    dt_items['mkd'] = "["+dt_items['title']+"]"+"("+dt_items['url']+")  \n"

# filter items for each user
    for i in range(len(unique_key)):
        dt_word_key = dt_word[dt_word['sckey']==unique_key[i]]
        key = unique_key[i]
        user = dt_word_key['user'].unique()
        words = dt_word_key['word']
        contents = []
        title = []

        for w in words:
            idx = dt_items['title'].str.contains(w,case=False)
            if any(idx)==True:
                cur.execute("UPDATE word_subscribe SET counts=counts+%s WHERE word=%s and sckey=%s",(sum(idx),w,key))
                cur.connection.commit()
                contents.append([w+'  \n',dt_items['mkd'][idx].str.cat()+'  \n'])
                title.append(w)
                print("[%s] User:%s\t\tWord:%s\t\tCount:%d" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'),user,w,sum(idx)))

        if len(title)>1:
            title = '+'.join(title)
            contents = [x for b in contents for x in b]
            contents = ''.join(contents)
            print(contents)
            url = 'https://sc.ftqq.com/'+key+'.send?'+'text='+title+'&desp='+contents
            rtn = urllib.request.urlopen(quote(url,safe=":?=/&"))
        elif len(title)==1:
            title = title[0]
            content = contents[0][1]
            url = 'https://sc.ftqq.com/'+key+'.send?'+'text='+title+'&desp='+content
            rtn = urllib.request.urlopen(quote(url,safe=":?=/&"))
        else:
            pass
