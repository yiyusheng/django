# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Max,Q,Count
from django.utils import timezone
from Prichat.models import ChatLogs,WordCount,WordCountHourly
from datetime import datetime,timedelta

import pandas as pd
import numpy as np
import pyecharts as pe
import json, math, time

REMOTE_HOST = "https://pyecharts.github.io/assets/js"

# keyword display
def word(request):
    # REQUEST.GET: get keywords
    getDict = request.GET
    permit_key = ['k1','k2','k3','k4','k5','k6','k7','k8','k9','k10']
    valueLists=[]
    if len(set(permit_key).intersection(getDict.keys()))==0:
        valueLists=['大饼','btc','bch','ltc','eos','eth','etc']
        len_keys = len(valueLists)
    else:
        keys = list(set(permit_key).intersection(getDict.keys()))
        len_keys = len(keys)
        for k in keys:
            valueLists.append(getDict[k])

    if 'type' in request.GET and request.GET['type']=='number':
        typeFlag = 0 #number
    else:
        typeFlag = 1 #frequent

    # REQUEST.GET: interval for scaling time
    if 'time' in request.GET:
        time_unit = getDict['time']
        if time_unit.isdigit() and int(time_unit)>0 and int(time_unit)<144*60*60*60*60*60*60*60*60:
            time_unit = int(time_unit)
        else:
            time_unit = 480
    else:
        time_unit = 480

    # REQUEST.GET: get recent days data 
    if 'days' in request.GET and getDict['days'].isdigit():
        days = int(getDict['days'])
    else:
        days = 30

    # QUERY DATA
    df = pd.DataFrame()
    now = timezone.now()
    day_ago = now - timedelta(days=days)
    od = WordCountHourly.objects.filter(time__range=[day_ago,now])
    for i in range(len_keys):
        object_data = od.filter(word__iexact=valueLists[i]).values('time','word','count','weighted_count')
        tmp_df = pd.DataFrame(list(object_data))
        if(len(tmp_df)==0):
            continue
        # merge for different case
        if len(pd.unique(tmp_df['word']))!=1:
            tmp_df = tmp_df.groupby('time').agg({'count':'sum','weighted_count':'sum'})
            tmp_df = tmp_df.reset_index()
            tmp_df['word'] = valueLists[i]
        df = pd.concat([df,tmp_df])

    if len(df)==0:
        return HttpResponse('<h1>Word was not found</h1>')
    # SCALE DATA
    df['time'] = pd.to_datetime(df['time'],format='%Y-%m-%d %H:%M')
    df['time'] = df['time'].values.astype(np.int64)//10**9
    df['time'] = df['time'].apply(lambda x: datetime.utcfromtimestamp(x/time_unit/60*time_unit*60))
    df = df.groupby(['time','word']).agg({'count':'sum','weighted_count':'sum'})
    df['weighted_count'] = np.array(df['weighted_count'],dtype=float)*100
    df['weighted_count'] = df['weighted_count'].round(2)
    df = df.reset_index()
    words_unique = pd.unique(df['word'])

    df_number = df.pivot_table(index='time',columns='word',values='count')
    df_number = df_number.fillna(0)
    df_number = df_number.reset_index()
    df_number.time = df_number.time.dt.tz_localize('UTC').dt.tz_convert('Asia/Shanghai')

    df_frequent = df.pivot_table(index='time',columns='word',values='weighted_count')
    df_frequent = df_frequent.fillna(0)
    df_frequent = df_frequent.reset_index()
    df_frequent.time = df_frequent.time.dt.tz_localize('UTC').dt.tz_convert('Asia/Shanghai')

    # PLOT FIGURES
    fg_number = pe.Line(title='关键词数量趋势',
          width=1600,height=450,title_top='50%',title_pos='center')
    fg_frequent = pe.Line(title='关键词频率趋势(每百句话中出现次数)',
          width=1600,height=450,title_top='6%',title_pos='center')
    for w in words_unique:
        fg_frequent.add(w,df_frequent.time,df_frequent[w])
        fg_number.add(w,df_number.time,df_number[w])
        #fg_number.add(w,df_number.index,df_number[w],is_datazoom_show=True)

    grid = pe.Grid(width=1600,height=900)
    grid.add(fg_frequent,grid_bottom='55%',grid_width=1300,grid_height=300)
    grid.add(fg_number,grid_top='55%',grid_width=1300,grid_height=300)

    # GENERATE HTML
    myechart=grid.render_embed()
    host=REMOTE_HOST
    script_list=grid.get_js_dependencies()
    return render(request,"word.html",
                        {"myechart":myechart,
                        "host":host,
                        "script_list":script_list})

