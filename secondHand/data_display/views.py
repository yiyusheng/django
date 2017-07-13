# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from data_display.models import Sh0713

def data_display(request):
    item_list = Sh0713.objects.order_by('-id')[:100]
    return(render(request,'data_display/data_display.html',{'list':item_list}))
