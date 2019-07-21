from Prichat.pyechart_json import json_response,json_error
from Prichat.data_XBTUSD import price
from pyecharts.charts import Kline
from pyecharts import options as opts

import json
from datetime import datetime,timedelta
from random import randrange

from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from rest_framework.views import APIView
import urllib.parse as urlparse
from urllib.parse import urlencode

JsonResponse = json_response
JsonError = json_error

def kline_base(df) -> Kline:
    df_values = df[['open','close','low','high']].values.tolist()
    df_time = df['time'].dt.strftime('%Y-%m-%d %H:%M:%S').values.tolist()
    fig = (
            Kline(init_opts=opts.InitOpts(width="1366px", height="768px"))
            .add_xaxis(df_time)
            .add_yaxis('Price',df_values)
            .set_global_opts(
                yaxis_opts=opts.AxisOpts(is_scale=True),
                xaxis_opts=opts.AxisOpts(
                    type_=None,is_scale=True,
                    splitarea_opts=opts.SplitAreaOpts(is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1))),
                datazoom_opts=[opts.DataZoomOpts()],
                title_opts=opts.TitleOpts(title="XBTUSD-k线图"),
                )
            .dump_options()
            )
    return fig

class ChartView(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(kline_base(price(request,'XBTUSD'))))

class IndexView(APIView):
    def get(self, request, *args, **kwargs):
        # parse get data
        end_time = timezone.now()
        end_time = end_time.replace(microsecond=0)
        start_time = end_time + timedelta(days=-3)

        getDict = request.GET
        client_timezone = ""
        #client_timezone = "+08:00"
        start_time = (len(getDict)>0 and 'start_time' in getDict) and getDict['start_time']+client_timezone or start_time
        end_time = (len(getDict)>0 and 'end_time' in getDict) and getDict['end_time']+client_timezone or end_time
        last_days = (len(getDict)>0 and 'last_days' in getDict) and getDict['last_days'] or '3'
        time_unit = (len(getDict)>0 and 'time_unit' in getDict) and getDict['time_unit'] or '60'

        if isinstance(start_time,str):
            start_time = datetime.strptime(start_time,"%Y-%m-%d %H:%M:%S")+timedelta(hours=8)
        if isinstance(end_time,str):
            end_time = datetime.strptime(end_time,"%Y-%m-%d %H:%M:%S")+timedelta(hours=8)

        paras = {'start_time': start_time.timestamp(),
                'end_time': end_time.timestamp(),
                'last_days': last_days,
                'time_unit': time_unit,}

        prefix = request.build_absolute_uri('/').strip("/")
        url = prefix+"/prichat/data_xbtusd/"
        url_parts = list(urlparse.urlparse(url))
        url_parts[4] = urlencode(paras)
        url = urlparse.urlunparse(url_parts)

        return render(request,'xbtusd.html',{
            'start_time': start_time,
            'end_time': end_time,
            'last_days': last_days,
            'time_unit': time_unit,
            'url':url,
            'title':'XBTUSD',})
        #return HttpResponse(content=open("./templates/xbtusd.html").read())
