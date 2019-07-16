# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pandas as pd
import numpy as np
import pyecharts.charts as pe
import json, math, time, pytz

from django.template import loader
from django.shortcuts import render
from django.db.models import Max,Q,Count
from django.utils import timezone
from django.http import HttpResponse

from Prichat.models import ChatLogs,WordCount,WordCountHourly
from Prichat.models import ChatLogs,WordCount,WordCountHourly,BitmexPrice
from datetime import datetime,timedelta
from pyecharts import options as opts
from pyecharts import components as cpns
from pyecharts.charts import Kline
from pyecharts.charts import Bar
from pyecharts.globals import CurrentConfig
from jinja2 import Environment, FileSystemLoader

CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./Prichat/templates"))

def get_chatlogs_count_group(days,time_unit):
    blackList = [
      'python-qqbot交流群',
      '青瑶的音乐交流群一群',
      'AppleTV喵群',
      'splatoon乌贼幼稚园',
      '玩鱼雷的踢了.jpg',
      '冬瓜的菜园子',
      '大武汉BTC群',
      'splatoon乌贼烧烤大排档',
      '比记金牌炒米粉店再次',
        ]
  # get data
    select_data = {"timeh": """DATE_FORMAT(time,'%%Y-%%m-%%d %%H:00')"""}
    now = timezone.now()                                                                       
    day_ago = now - timedelta(days=days)
    od = ChatLogs.objects.filter(time__range=[day_ago,now])

    dt_raw = od.extra(select=select_data).values('group_name','timeh').order_by().annotate(count=Count('group_name')).values('group_name','timeh','count')
    dt = pd.DataFrame(list(dt_raw))
    dt = dt[~dt['group_name'].str.contains('uin')]

  # SCCALE DATA
    dt['timeh'] = pd.to_datetime(dt['timeh'],format='%Y-%m-%d %H:%M')
    dt['timeh'] = dt['timeh'].values.astype(np.int64)//10**9
    dt['timeh'] = dt['timeh'].apply(lambda x: datetime.utcfromtimestamp(int(x/time_unit/60)*time_unit*60))
    dt = dt.groupby(['timeh','group_name']).agg({'count':'sum'})
    dt = dt.reset_index()

  # DCAST data
    group_name_unique = pd.unique(dt['group_name'])
    group_name_unique = np.setdiff1d(group_name_unique,np.array(blackList))
    dt = dt.pivot_table(index='timeh',columns='group_name',values='count')
    dt = dt.fillna(0)
    dt = dt.reset_index()
    dt.timeh = dt.timeh.dt.tz_localize('UTC').dt.tz_convert('Asia/Shanghai')

    return dt

def group(request):
    # 可视化展示页面
    if 'days' in request.GET and request.GET['days'].isdigit():
        days = int(request.GET['days'])
    else:
        days = 14

    if 'time' in request.GET and request.GET['time'].isdigit():
        time_unit = int(request.GET['time'])
        time_unit = max(60,min(time_unit,1440*7))
    else:
        time_unit = 60

    dt=get_chatlogs_count_group(days,time_unit)

    # PLOT FIGURES
    df_values = dt['Bitmex'].values.tolist()
    df_time = dt['timeh'].dt.strftime('%Y-%m-%d %H:%M:%S').values.tolist()
    print(df_values[0:2],df_time[0:2],len(dt))
    fig = (
        Bar(init_opts=opts.InitOpts(width="1366px", height="768px"))
        .add_xaxis(df_time)
        .add_yaxis(series_name="bar", yaxis_data=df_values, label_opts=opts.LabelOpts(is_show=False)
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Bitmex每小时聊天记录数"),
            xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=False)),
            yaxis_opts=opts.AxisOpts(
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            datazoom_opts=[opts.DataZoomOpts()],
        )
    )
    return HttpResponse(fig.render_embed())
