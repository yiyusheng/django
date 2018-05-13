# -*- coding: utf-8 -*-
import pymysql,warnings,jieba,sys
import pandas as pd
from datetime import datetime,timedelta
from collections import Counter

# mysql connect
def sqlcon():
    conn = pymysql.connect(
        host = "localhost",
        user = "root",
        passwd = "qwer1234",
        charset = "utf8",
        database = 'prichat'
    )   
    return conn

# get data from table chat_logs for one hour
def get_chats(sc,ts_now,all=False):
    cursor = sc.cursor()
    if all:
        sql = "SELECT content FROM chat_logs"
    else:
        sql = "SELECT content FROM chat_logs WHERE date_format(time,'%%Y-%%m-%%d %%H:00:00')=%s" 
    cursor.execute(sql,(ts_now.strftime('%Y-%m-%d %H:%M:%S')))
    data = cursor.fetchall()
    data = [d[0] for d in data]
    return data
    
# parse these data with jieba
def data_parse(data):
    word_list = [list(jieba.cut(d,cut_all=False)) for d in data]
    word_list = [i for a in word_list for i in a]
    return word_list

# store them to table word_count and word_count_hourly
def word_insert(sc,word_count,ts_now,len_logs):
    cursor = sc.cursor()
    df = pd.DataFrame(list(word_count.items()),columns=['word','count'])
    df['weighted_count'] = df['count']/len_logs
    df['weighted_count'] = df['weighted_count'].round(4)
    df['time'] = ts_now.strftime('%Y-%m-%d %H:%M:%S')

    # for hourly count
    sql = "INSERT INTO word_count_hourly(time,word,count,weighted_count) VALUES(%s,%s,%s,%s)"
    cursor.executemany(sql,df[['time','word','count','weighted_count']].values.tolist())
    cursor.connection.commit()

    # for total count
    sql = "INSERT INTO word_count(time,word,count) VALUES(%s,%s,%s) ON DUPLICATE KEY UPDATE count=count+%s"
    for i in range(len(df)):
        cursor.execute(sql,(df['time'][i],df['word'][i],str(df['count'][i]),str(df['count'][i])))
        cursor.connection.commit()

    


if __name__=='__main__':
    argv = sys.argv
    #ts_now = datetime.strptime(argv[1],'%Y-%m-%dT%H:%M:%S')
    if len(argv)==2:
        ts_now = datetime.strptime(argv[1],'%Y-%m-%dT%H:%M:%S')
        print 'special time:%s' %(ts_now)
    else:
        # for last hour
        ts_now = datetime.now().replace(minute=0,second=0,microsecond=0)-timedelta(hours=1)
    sc = sqlcon()
    data = get_chats(sc,ts_now)
    word_list = data_parse(data)
    word_count = Counter(word_list)
    word_insert(sc,word_count,ts_now,len(data))
