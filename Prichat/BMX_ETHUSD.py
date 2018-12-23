# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Max,Q,Count
from django.utils import timezone
from Prichat.models import ChatLogs,WordCount,WordCountHourly,BitmexPrice
from datetime import datetime,timedelta

import pandas as pd
import numpy as np
import pyecharts as pe
import json, math, time, pytz

REMOTE_HOST = "https://pyecharts.github.io/assets/js"

# keyword display
def price(request):
    # REQUEST.GET: get keywords
    getDict = request.GET
    if 'days' in request.GET and getDict['days'].isdigit():
        days = int(getDict['days'])
    else:
        days = 7

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
    df['time'] = df['time'].apply(lambda x: datetime.utcfromtimestamp(x/time_unit/60*time_unit*60))
    df = df.groupby(['time','symbol']).agg({'open':'first',
                                   'low':'min',
                                   'high':'max',
                                   'close':'last',
                                   'volume':'sum'})
    df = df.reset_index()
    df.time = df.time.dt.tz_localize('UTC').dt.tz_convert('Asia/Shanghai')

    # PLOT FIGURES
    df_values = df[['open','close','low','high']].values.tolist()
    fg = pe.Kline(title='k线图',
          width=1600,height=900,title_top='3%',title_pos='center')
    fg.add(df['symbol'][0],df['time'],df_values,is_datazoom_show=True,mark_point=['max','min'])

    # GENERATE HTML
    myechart=fg.render_embed()
    host=REMOTE_HOST
    script_list=fg.get_js_dependencies()
    return render(request,"price.html",
                        {"myechart":myechart,
                        "host":host,
                        "script_list":script_list})

