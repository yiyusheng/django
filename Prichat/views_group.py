# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Max,Q
from django.db.models import Count
from Prichat.models import ChatLogs,WordCount,WordCountHourly
from datetime import datetime,timedelta
from django.utils import timezone

import pandas as pd
import numpy as np
import pyecharts as pe
import json, math, time

REMOTE_HOST = "https://pyecharts.github.io/assets/js"
def get_chatlogs_count():
    # get data
    select_data = {"timeh": """DATE_FORMAT(time,'%%Y-%%m-%%d %%H:00')"""}
    dt_raw = ChatLogs.objects.extra(select=select_data).values('timeh').annotate(count=Count('content')).values('timeh','count')
    dt = pd.DataFrame(list(dt_raw))
    dt['timeh'] = pd.to_datetime(dt['timeh'],format='%Y-%m-%d %H:%M')

  # package data
    dt['timeh'] = dt['timeh'].dt.tz_convert('Asia/Shanghai')
    fg = pe.Bar('每小时聊天记录数',
          width=1600,height=900,title_pos='center',title_top='bottom')
    fg.add('数量',dt['timeh'],dt['count'])
    return fg

def get_chatlogs_count_group(days):

  # get data
    select_data = {"timeh": """DATE_FORMAT(time,'%%Y-%%m-%%d %%H:00')"""}
    now = timezone.now()                                                                       
    day_ago = now - timedelta(days=days)
    od = ChatLogs.objects.filter(time__range=[day_ago,now])

    dt_raw = od.extra(select=select_data).values('group_name','timeh').order_by().annotate(count=Count('group_name')).values('group_name','timeh','count')
    dt = pd.DataFrame(list(dt_raw))

  # prepare data
    dt['timeh'] = pd.to_datetime(dt['timeh'],format='%Y-%m-%d %H:%M')
    group_name_unique = pd.unique(dt['group_name'])
    dt = dt.pivot_table(index='timeh',columns='group_name',values='count')
    dt = dt.fillna(0)
    dt = dt.reset_index()
    dt.timeh = dt.timeh.dt.tz_localize('UTC').dt.tz_convert('Asia/Shanghai')

  # package data into object of pyecharts
    fg = pe.Bar(title='各群每小时聊天记录数',
          width=1600,height=900,title_pos='center',title_top='3%')
    for gn in group_name_unique:
        fg.add(gn,dt.timeh,dt[gn],is_stack=True,is_balel_show=True,is_datazoom_show=True)
    
  # return
    return fg

def group(request):
    # 可视化展示页面
    if 'days' in request.GET and getDict['days'].isdigit():
        days = int(getDict['days'])
    else:
        days = 14

    fg = get_chatlogs_count_group(days)

    myechart=fg.render_embed()
    host=REMOTE_HOST
    script_list=fg.get_js_dependencies()
    return render(request,"group.html",
                        {"myechart":myechart,
                        "host":host,
                        "script_list":script_list})
