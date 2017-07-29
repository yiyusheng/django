# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from show.models import Secondhand
from datetime import datetime,timedelta

def show(request):
    # Data proprepare
    enddate = datetime.utcnow()
    startdate = enddate + timedelta(days=-1)
    webname = Secondhand.objects.values('webname').distinct()
    webnameList = [i.values()[0] for i in list(webname)]
    maxItems = 2000
    
    # extract data 
    getDict = request.GET
    getWebname = len(getDict)>0 and set(webnameList).intersection(getDict.keys()) or ''
    keywords = (len(getDict)>0 and 'keywords' in getDict) and getDict['keywords'] or ''
    
    keywords = keywords.strip()
    
    if keywords=='' and len(getWebname)==0:
        item_list = Secondhand.objects.filter(create_time__range=[startdate,enddate]).order_by('-time')[:maxItems]
    elif keywords!='' and len(getWebname)==0:
        item_list = Secondhand.objects.filter(title__contains=keywords).order_by('-time')[:maxItems]
    else:
        item_list = Secondhand.objects.filter(webname__in=getWebname,title__contains=keywords).order_by('-time')[:maxItems]
    
    # return
    return(render(request,'show.html',
        {'item_list':item_list,
         'len_list': len(item_list),
         'webname': webname}))