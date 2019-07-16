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

from Prichat.models import ChatLogs,WordCount,WordCountHourly,BitmexPrice
from datetime import datetime,timedelta
from pyecharts import options as opts
from pyecharts import components as cpns
from pyecharts.charts import Kline
from pyecharts.globals import CurrentConfig
from jinja2 import Environment, FileSystemLoader

CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./Prichat/templates"))


# keyword display
def price(request):
    # REQUEST.GET: get keywords
    getDict = request.GET
    if 'days' in request.GET and getDict['days'].isdigit():
        days = int(getDict['days'])
    else:
        days = 3

    if 'time' in request.GET and getDict['time'].isdigit():
        time_unit = int(getDict['time'])
    else:
        time_unit = 60

    # QUERY DATA
    now = timezone.now()
    day_ago = now - timedelta(days=days)
    od = BitmexPrice.objects.filter(timestamp__range=[day_ago,now],symbol='ETHUSD').values('timestamp','symbol','open','high','low','close','volume')
    df = pd.DataFrame(list(od))
    df['time'] = pd.to_datetime(df['timestamp'],format='%Y-%m-%d %H:%M')
    df['open'] = pd.to_numeric(df['open'])
    df['low'] = pd.to_numeric(df['low'])
    df['high'] = pd.to_numeric(df['high'])
    df['close'] = pd.to_numeric(df['close'])
    df['volume'] = pd.to_numeric(df['volume'])

    # SCALE DATA
    df['time'] = df['time'].values.astype(np.int64)//10**9
    df['time'] = df['time'].apply(lambda x: datetime.utcfromtimestamp(int(x/time_unit/60)*time_unit*60))
    print(df['time'])
    df = df.groupby(['time','symbol']).agg({'open':'first',
                                   'low':'min',
                                   'high':'max',
                                   'close':'last',
                                   'volume':'sum'})
    df = df.reset_index()
    df.time = df.time.dt.tz_localize('UTC').dt.tz_convert('Asia/Shanghai')

    # PLOT FIGURES
    df_values = df[['open','close','low','high']].values.tolist()
    df_time = df['time'].dt.strftime('%Y-%m-%d %H:%M:%S').values.tolist()
    print(df_time[0:2],df_values[0:2],len(df_time),len(df_values))
    fig = (
            Kline(init_opts=opts.InitOpts(width="1680px", height="800px"))
            .add_xaxis(df_time)
            .add_yaxis('Price',df_values)
            .set_global_opts(
		yaxis_opts=opts.AxisOpts(is_scale=True),
		xaxis_opts=opts.AxisOpts(
                    type_=None,is_scale=True,
                    splitarea_opts=opts.SplitAreaOpts(is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1))),
                datazoom_opts=[opts.DataZoomOpts()],
                title_opts=opts.TitleOpts(title="ETHUSD-k线图"),
                )
            )

    return HttpResponse(fig.render_embed())
