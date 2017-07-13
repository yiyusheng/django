# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from data_display.models import Secondhand

def data_display(request):
    item_list = Secondhand.objects.order_by('-create_time')[:500]
    return(render(request,'data_display/data_display.html',{'list':item_list}))
