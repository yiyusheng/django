# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from show.models import Secondhand
from datetime import datetime,timedelta

def show(request):
    # extract data
    enddate = datetime.utcnow()
    startdate = enddate + timedelta(days=-1)
    item_list = Secondhand.objects.filter(create_time__range=[startdate,enddate]).order_by('-create_time')

    # reduce items to less than 2000
    if len(item_list)>2000:
        item_list = item_list[:2000]

    # process
    len_list = len(item_list)
    for i in range(len_list):
        item_list[i].create_time += timedelta(hours=+8)
        item_list[i].ext2 = item_list[i].ext2==None and '-1' or item_list[i].ext2

    # return
    return(render(request,'show/show.html',
        {'item_list':item_list,
         'len_list': len_list}))
