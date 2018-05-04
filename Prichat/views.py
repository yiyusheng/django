# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Max,Q
from django.db.models import Count

from Prichat.models import ChatLogs,WordCount,WordCountHourly
from datetime import datetime
import pandas as pd, pyecharts as pe, json, math

REMOTE_HOST = "https://pyecharts.github.io/assets/js"

# Create your views here.
def person(request):
  getDict = request.GET
  if len(getDict) == 0:
    nn = 'AK'
  else:
    nn = getDict['nickname']
  # Get chat logs from special name
  object_cl = ChatLogs.objects.filter(nickname = nn).order_by('-create_time')
  object_wch_word = ChatLogs.objects.values('nickname').distinct()
  return render(request,'display/person.html',
      {'cl':object_cl})

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
    return render(request,"display/group.html",
                        {"myechart":myechart,
                        "host":host,
                        "script_list":script_list})

# keyword display
def word(request):
  getDict = request.GET
    
  if len(getDict) == 1:
    word = getDict['keyword']
  else:
    word = '大饼'
  object_wch_word = WordCountHourly.objects.filter(word = word).values('create_time','count')
  df = pd.DataFrame(list(object_wch_word))
  if len(df) > 1:
    df.index = df['create_time']
    df_hour = df.resample('H').sum()
    df_day = df.resample('D').sum()

    df_out = df_day
    count = df_out['count'].tolist()
    create_time = [i.strftime('%Y-%m-%d %H:%M') for i in df_out.index.tolist()]
    return render(request, 'display/word.html',
       {
        'count':        json.dumps(count),
        'create_time':  json.dumps(create_time),
        'keyword':         json.dumps(word),
        })
