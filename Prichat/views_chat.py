# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Max,Q
from django.db.models import Count
from Prichat.models import ChatLogs,WordCount,WordCountHourly
from datetime import datetime

import pandas as pd
import numpy as np
import pyecharts as pe
import json, math, time

REMOTE_HOST = "https://pyecharts.github.io/assets/js"

# Create your views here.
def chat(request):
# Parse request
    groupFlag = False
    nameFlag = False
    keywordFlag = False
    if 'group' in request.GET:
        group = request.GET['group']
        groupFlag = True

    if 'name' in request.GET:
        name = request.GET['name']
        nameFlag = True

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        keywordFlag = True

# generate nameList and groupList
    nameList = ['AK','空深空','天乐','trdxz','八哥谈币','梦雨','BitMEX_Jack','神级','鱼籽','钱来来','落叶风双','古乐天','Goldman Sachs']
    groupList = ChatLogs.objects.values('group_name').distinct()
    groupList = [i.values()[0] for i in list(groupList)]

# Get chat logs from special name
    maxItems = 1000
    co = ChatLogs.objects.exclude(content='')
    if keywordFlag:
        data = co.filter(content__icontains=keyword).order_by('-time')[:maxItems]
    else:
        if groupFlag and not nameFlag:
            data = co.filter(group_name=group).order_by('-time')[:maxItems]
        elif nameFlag and not groupFlag:
            data = co.filter(user = name).order_by('-time')[:maxItems]
        elif groupFlag and nameFlag:
            data = co.filter(group_name=group,user = name).order_by('-time')[:maxItems]
        else:
            data = co.filter(group_name = '爆仓疗养院').order_by('-time')[:maxItems]
    
    
    return render(request,'chat.html',
            {'cl':data,
            'group_name':groupList,
            'user':nameList})
