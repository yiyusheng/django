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
    invalidWebList = ['dospy','gfanWeb','it168','smzdm','tgbusWeb','imp3']
    validWebList = list(set(webnameList) - set(invalidWebList))
    validWebList.sort()
    invalidWebList.sort()

    whiteList = [
            'mac','mbp','ipod','ipad','watch','airpod',
            'surface','miix','yoga','venue','thinkpad','xps',
            'kindle','kpw','ps4','psv','xbox','switch','ns',
            'ikbc','电动车',
            '1050','1060','1070','1080'
            ]
    blackList = ['口红','喷雾','悦木之源','裤',
            '鞋','耐克','子弹头','裙','乳液','短袖','衣','靴',
            '吸奶器','精华露','霜','面膜','眼影',
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
        maxItems = 200 
        item_list = so.filter(create_time__range=[day1ago,now]).order_by('-time')[:maxItems]
    else:
        if keyword!='':
            if keyword=='customized':
                so = so.filter(create_time__range=[day3ago,now]).filter(reduce(operator.or_, [Q(title__icontains=q) for q in whiteList]))
                so = so.exclude(reduce(operator.or_, [Q(title__icontains=q) for q in blackList]))
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
            maxItems = 200 
        if uname!='':
            so = so.filter(uname=uname)
            maxItems = 1000 
        item_list = so.order_by('-time')[:maxItems]
    
    # return
    return(render(request,'secondhand.html',
        {'item_list':item_list,
         'len_list': len(item_list),
         'validSite': validWebList,
         'invalidSite': invalidWebList,
         'server_time':now,
         'seller_time':seller_update_time['update_time__max'],
         }))
