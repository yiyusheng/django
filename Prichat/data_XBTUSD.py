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
def price(request,sbl):
    end_time = timezone.now()
    end_time = end_time.replace(microsecond=0)
    start_time = end_time + timedelta(days=-3)
    # REQUEST.GET: get keywords
    getDict = request.GET
    start_time = (len(getDict)>0 and 'start_time' in getDict) and getDict['start_time'] or start_time.timestamp()
    end_time = (len(getDict)>0 and 'end_time' in getDict) and getDict['end_time'] or end_time.timestamp()
    last_days = (len(getDict)>0 and 'last_days' in getDict) and getDict['last_days'] or '3'
    time_unit = (len(getDict)>0 and 'time_unit' in getDict) and getDict['time_unit'] or '60'
    if isinstance(start_time,str):
        start_time = datetime.fromtimestamp(float(start_time))
        start_time = pytz.utc.localize(start_time)
    if isinstance(end_time,str):
        end_time = datetime.fromtimestamp(float(end_time))
        end_time = pytz.utc.localize(end_time)
    last_days = int(last_days)
    time_unit = int(time_unit)

    # QUERY DATA
    od = BitmexPrice.objects.filter(timestamp__range=[start_time,end_time],symbol=sbl).values('timestamp','symbol','open','high','low','close','volume')
    df = pd.DataFrame(list(od))
    df['time'] = pd.to_datetime(df['timestamp'],format='%Y-%m-%d %H:%M')
    df['open'] = pd.to_numeric(df['open'])
    df['low'] = pd.to_numeric(df['low'])
    df['high'] = pd.to_numeric(df['high'])
    df['close'] = pd.to_numeric(df['close'])
    df['volume'] = pd.to_numeric(df['volume'])
    df = df[df['low']!=0]
    print(len(df))

    # SCALE DATA
    df['time'] = df['time'].values.astype(np.int64)//10**9
    df['time'] = df['time'].apply(lambda x: datetime.utcfromtimestamp(int(x/time_unit/60)*time_unit*60))
    df = df.groupby(['time','symbol']).agg({'open':'first',
                                   'low':'min',
                                   'high':'max',
                                   'close':'last',
                                   'volume':'sum'})
    df = df.reset_index()
    df.time = df.time.dt.tz_localize('UTC').dt.tz_convert('Asia/Shanghai')

    return df
