# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from show.models import Secondhand
from datetime import datetime,timedelta

def show(request):
    # extract data
    enddate = datetime.utcnow()
    startdate = enddate + timedelta(days=-1)
    
    if request.method == 'GET' and 'keywords' in request.GET and len(request.GET['keywords'])>0 and ('webname' not in request.GET or len(request.GET['webname'])==0):
        item_list = Secondhand.objects.filter(title__contains=request.GET['keywords']).order_by('-time')
    elif request.method == 'GET' and 'webname' in request.GET and len(request.GET['webname'])>0 and ('keywords' not in request.GET or len(request.GET['keywords'])==0):
        item_list = Secondhand.objects.filter(webname=request.GET['webname']).order_by('-time')[:2000]
    elif request.method == 'GET' and 'webname' in request.GET and len(request.GET['webname'])>0 and 'keywords' in request.GET and len(request.GET['keywords'])>0 :
        item_list = Secondhand.objects.filter(webname=request.GET['webname'],title__contains=request.GET['keywords']).order_by('-time')[:2000]
    else:
        item_list = Secondhand.objects.filter(create_time__range=[startdate,enddate]).order_by('-time')[:2000]
    
    # process
    len_list = len(item_list)
    webname = Secondhand.objects.values('webname').distinct()

    # return
    return(render(request,'show.html',
        {'item_list':item_list,
         'len_list': len_list,
         'webname': webname}))