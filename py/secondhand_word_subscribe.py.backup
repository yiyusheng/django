# -*- coding:utf-8 -*-                                                                         
import requests, time, pymysql, urllib, re
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
        desp = []
        text = []

        for w in words:
            idx = dt_items['title'].str.contains(w,case=False)
            if any(idx)==True:

                # if the first former char of unique_key[i] is alpha and the first following char of unique_key[i] is alpha then remove the item
                unique_key_split = dt_items['title'][idx].apply(lambda x: re.split(w,x,flags=re.IGNORECASE))
                char_former = unique_key_split.apply(lambda x: True if len(x[0])==0 else not x[0][-1].isalpha())
                char_follower = unique_key_split.apply(lambda x: True if len(x[1])==0 else not x[1][0].isalpha())
                idx = idx & (char_former | char_follower)

                if any(idx)==True:
                    cur.execute("UPDATE word_subscribe SET counts=counts+%s WHERE word=%s and sckey=%s",(sum(idx),w,key))
                    cur.connection.commit()
                    desp.append([w+'  \n',dt_items['mkd'][idx].str.cat()+'  \n'])
                    text.append(w)
                    print("[%s] User:%s\t\tWord:%s\t\tCount:%d" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'),user,w,sum(idx)))

        if len(text)>1:
            text = '+'.join(text)
            desp = [x for b in desp for x in b]
            desp = ''.join(desp)
            url = 'https://sc.ftqq.com/'+key+'.send?'+'text='+text+'&desp='+desp
            rtn = urllib.request.urlopen(quote(url,safe=":?=/&"))
        elif len(text)==1:
            text = text[0]
            content = desp[0][1]
            url = 'https://sc.ftqq.com/'+key+'.send?'+'text='+text+'&desp='+content
            rtn = urllib.request.urlopen(quote(url,safe=":?=/&"))
        else:
            pass
