# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from show.models import Secondhand,Advertiser
from datetime import datetime,timedelta
from django.db.models import Max

def show(request):
    # Data proprepare
    now = datetime.utcnow()
    day1ago = now + timedelta(days=-1)
    webname = Secondhand.objects.values('webname').distinct()
    seller_update_time = Advertiser.objects.all().aggregate(Max('update_time'))
    webnameList = [i.values()[0] for i in list(webname)]
    maxItems = 2000 
    
    # extract data 
    getDict = request.GET
    getWebname = len(getDict)>0 and set(webnameList).intersection(getDict.keys()) or ''
    keywords = (len(getDict)>0 and 'keywords' in getDict) and getDict['keywords'] or ''
#    keywords = keywords.strip()
    uname = (len(getDict)>0 and 'uname' in getDict) and getDict['uname'] or ''
    so = Secondhand.objects.extra(select={'is_ad':
            '''SELECT * FROM secondHand WHERE NOT EXIST 
            (SELECT 1 FROM advertiser ad WHERE ad.uname=sh.uname AND ad.webname=sh.webname'''})
    so = Secondhand.objects.extra(
            tables = ['advertiser'],
            where = ['advertiser.uname=secondHand.uname or advertiser.webname=secondHand.webname'],
            )
    so = Secondhand.objects.filter(advertiser=0)
    
    if len(keywords)+len(getWebname)+len(uname)==0 or len(getDict)==0:
        item_list = so.filter(create_time__range=[day1ago,now]).order_by('-time')[:maxItems]
    else:
        if keywords!='':
            so = so.filter(title__icontains=keywords)
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