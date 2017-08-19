# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from show.models import Secondhand,Advertiser
from datetime import datetime,timedelta
from django.db.models import Max,Q
import operator

def show(request):
    # Data proprepare
    now = datetime.utcnow()
    day1ago = now + timedelta(days=-1)
    day3ago = now + timedelta(days=-3)
    seller_update_time = Advertiser.objects.all().aggregate(Max('update_time'))

    webname = Secondhand.objects.values('webname').distinct()
    webnameList = [i.values()[0] for i in list(webname)]

    maxItems = 500 
    customList = ['mac','surface','xbox',
            'ps4','kindle','kpw','ipad',
            'thinkpad','iphone7','moto',
            'miix','xps','watch','new balance']
    
    # Get data 
    getDict = request.GET
    getWebname = len(getDict)>0 and set(webnameList).intersection(getDict.keys()) or ''
    keywords = (len(getDict)>0 and 'keywords' in getDict) and getDict['keywords'] or ''
    uname = (len(getDict)>0 and 'uname' in getDict) and getDict['uname'] or ''

    # Extract data
    ad = Advertiser.objects.filter(update_time__range=[day3ago,now]).values_list('uname',flat=True)
    so = Secondhand.objects.exclude(uname__in=ad)
    
    if len(keywords)+len(getWebname)+len(uname)==0 or len(getDict)==0:
        item_list = so.filter(create_time__range=[day1ago,now]).order_by('-time')[:maxItems]
    else:
        if keywords!='':
            if keywords=='customized':
                so = so.filter(reduce(operator.or_, [Q(title__icontains=q) for q in customList]))
                maxItems = 100
            else:
                so = so.filter(title__icontains=keywords)
                maxItems = 50
        if getWebname!='':
            so = so.filter(webname__in=getWebname)
        if uname!='':
            so = so.filter(uname=uname)
        item_list = so.order_by('-time')[:maxItems]
    
    # return
    return(render(request,'show.html',
        {'item_list':item_list,
         'len_list': len(item_list),
         'webname': webname,
         'server_time':now+timedelta(hours=8),
         'seller_time':seller_update_time['update_time__max'],
         }))
