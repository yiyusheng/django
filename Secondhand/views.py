# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from Secondhand.models import Secondhand,Advertiser
from datetime import datetime,timedelta
from django.db.models import Max,Q
from django.utils import timezone
import operator

def secondhand(request):
    # Data proprepare
    now = timezone.now()
    day1ago = now + timedelta(days=-1)
    day3ago = now + timedelta(days=-3)
    seller_update_time = Advertiser.objects.all().aggregate(Max('update_time'))

    webname = Secondhand.objects.values('webname').distinct()
    webnameList = [i.values()[0] for i in list(webname)]

    customList = [
            'mac','mbp','ipod','ipad','watch',
            'surface','miix','yoga','venue','thinkpad','xps',
            'kindle','kpw','ps4','psv','xbox','switch','ns',
            'ikbc',
            '1050','1060','1070','1080'
            ]
    
    # Get data 
    getDict = request.GET
    getWebname = len(getDict)>0 and set(webnameList).intersection(getDict.keys()) or ''
    keyword = (len(getDict)>0 and 'keyword' in getDict) and getDict['keyword'] or ''
    uname = (len(getDict)>0 and 'uname' in getDict) and getDict['uname'] or ''

    # Extract data
    ad = Advertiser.objects.filter(update_time__range=[day3ago,now]).values_list('uname',flat=True)
    so = Secondhand.objects.exclude(uname__in=ad)
    
    if len(keyword)+len(getWebname)+len(uname)==0 or len(getDict)==0:
        maxItems = 1000 
        item_list = so.filter(create_time__range=[day1ago,now]).order_by('-time')[:maxItems]
    else:
        if keyword!='':
            if keyword=='customized':
                so = so.filter(create_time__range=[day3ago,now]).filter(reduce(operator.or_, [Q(title__icontains=q) for q in customList]))
                maxItems = 200
            elif ' ' in keyword:
                split_keyword = keyword.split(' ')
                so = so.filter(reduce(operator.and_, [Q(title__icontains=q) for q in split_keyword]))
                maxItems = 100
            else:
                so = so.filter(title__icontains=keyword)
                maxItems = 100
        if getWebname!='':
            so = so.filter(webname__in=getWebname)
            maxItems = 1000 
        if uname!='':
            so = so.filter(uname=uname)
            maxItems = 1000 
        item_list = so.order_by('-time')[:maxItems]
    
    # return
    return(render(request,'show.html',
        {'item_list':item_list,
         'len_list': len(item_list),
         'webname': webname,
         'server_time':now+timedelta(hours=8),
         'seller_time':seller_update_time['update_time__max'],
         }))
