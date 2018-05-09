# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Max,Q
from django.db.models import Count
from Prichat.models import ChatLogs,WordCount,WordCountHourly
from datetime import datetime

import pandas as pd
import numpy as np
import pyecharts as pe
import json, math, time

REMOTE_HOST = "https://pyecharts.github.io/assets/js"


def get_chatlogs_count():
    # get data
    select_data = {"date": """DATE_FORMAT(create_time,'%%Y-%%m-%%d %%H:00')"""}
    dt_raw = ChatLogs.objects.extra(select=select_data).values('date').annotate(count=Count('content')).values('date','count')
    dt = pd.DataFrame(list(dt_raw))
    dt['date'] = pd.to_datetime(dt['date'],format='%Y-%m-%d %H:%M')

  # package data
    fg = pe.Bar('每小时聊天记录数',
          width=1600,height=900,title_pos='center',title_top='bottom')
    fg.add('数量',dt['date'],dt['count'])
    return fg

def get_chatlogs_count_group():

  # get data
    select_data = {"date": """DATE_FORMAT(create_time,'%%Y-%%m-%%d %%H:00')"""}
    dt_raw = ChatLogs.objects.extra(select=select_data).values('group_name','date').order_by().annotate(count=Count('group_name')).values('group_name','date','count')
    dt = pd.DataFrame(list(dt_raw))

  # prepare data
    dt['date'] = pd.to_datetime(dt['date'],format='%Y-%m-%d %H:%M')
    group_name_unique = pd.unique(dt['group_name'])
    dt = dt.pivot_table(index='date',columns='group_name',values='count')
    dt = dt.fillna(0)

  # package data into object of pyecharts
    fg = pe.Bar(title='各群每小时聊天记录数',
          width=1600,height=900,title_pos='center',title_top='3%')
    for gn in group_name_unique:
        fg.add(gn,dt.index,dt[gn],is_stack=True,is_balel_show=True,is_datazoom_show=True)
    
  # return
    return fg

def group(request):
    # 可视化展示页面
    fg = get_chatlogs_count_group()

    myechart=fg.render_embed()
    host=REMOTE_HOST
    script_list=fg.get_js_dependencies()
    return render(request,"group.html",
                        {"myechart":myechart,
                        "host":host,
                        "script_list":script_list})

# keyword display
def word(request):
# Recieve GET data
    getDict = request.GET
    permit_key = ['k1','k2','k3','k4','k5','k6','k7','k8','k9','k10']
    request_values=[]
    if len(getDict) == 0 or len(set(permit_key).intersection(getDict.keys()))==0:
        request_values=['btc','bch','ltc','eos','eth','etc']
        len_keys = len(request_values)
    else:
        keys = list(set(permit_key).intersection(getDict.keys()))
        len_keys = len(keys)
        for k in keys:
            request_values.append(getDict[k])

# Query data 
    df = pd.DataFrame()
    for i in range(len_keys):
        object_data = WordCountHourly.objects.filter(word__iexact=request_values[i]).values('create_time','word','count')
        tmp_df = pd.DataFrame(list(object_data))
        tmp_df = tmp_df.rename(columns={'create_time':'time'})
        if len(pd.unique(tmp_df['word']))!=1:
            tmp_df = tmp_df['count'].groupby(tmp_df['time']).sum()
            tmp_df = tmp_df.reset_index()
            tmp_df['word'] = request_values[i]
        df = pd.concat([df,tmp_df])

# Process data
    if len(list(set(['time']).intersection(getDict.keys())))!=0:
        time_unit = getDict['time']
        if time_unit.isdigit() and int(time_unit)>0 and int(time_unit)<144:
            time_unit = int(time_unit)
        else:
            time_unit = 6
    else:
        time_unit = 6

    df['time'] = pd.to_datetime(df['time'],format='%Y-%m-%d %H:%M')
    df['time'] = df['time'].values.astype(np.int64)//10**9
    df['time'] = df['time'].apply(lambda x: datetime.fromtimestamp(x/time_unit/3600*time_unit*3600))
    df = df['count'].groupby([df['time'],df['word']]).sum()
    df = df.reset_index()

    words_unique = pd.unique(df['word'])
    df = df.pivot_table(index='time',columns='word',values='count')
    df = df.fillna(0)

# Generate figure
    fg = pe.Line(title='关键词趋势',
          width=1600,height=900,title_pos='center',title_top='3%')
    for w in words_unique:
        fg.add(w,df.index,df[w],is_datazoom_show=True)
    for w in words_unique:
        1

    # Return data
    myechart=fg.render_embed()
    host=REMOTE_HOST
    script_list=fg.get_js_dependencies()
    return render(request,"word.html",
                        {"myechart":myechart,
                        "host":host,
                        "script_list":script_list})

# Create your views here.
def chat(request):
    groupFlag = False
    nameFlag = False
    keywordFlag = False
    if 'group' in request.GET:
        group = request.GET['group']
        groupFlag = True

    if 'name' in request.GET:
        name = request.GET['name']
        nameFlag = True

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        keywordFlag = True

    nameList = ['空深空','AK','天乐','trdxz','梦雨','BitMEX_Jack','神级','鱼籽']
    groupList = ChatLogs.objects.values('group_name').distinct()
    groupList = [i.values()[0] for i in list(groupList)]

    # Get chat logs from special name
    maxItems = 1000
    co = ChatLogs.objects.exclude(content='')
    if keywordFlag:
        data = co.filter(content__icontains=keyword).order_by('-create_time')[:maxItems]
    else:
        if groupFlag and not nameFlag:
            data = co.filter(group_name=group).order_by('-create_time')[:maxItems]
        elif nameFlag and not groupFlag:
            data = co.filter(nickname = name).order_by('-create_time')[:maxItems]
        elif groupFlag and nameFlag:
            data = co.filter(group_name=group,nickname = name).order_by('-create_time')[:maxItems]
        else:
            data = co.filter(nickname = 'AK').order_by('-create_time')[:maxItems]
    
    
    return render(request,'chat.html',
            {'cl':data,
            'group_name':groupList,
            'nickname':nameList})
