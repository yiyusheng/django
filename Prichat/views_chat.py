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
import json, math, time, operator

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
        split_keyword = keyword.split(' ')

    if 'name' not in request.GET and 'keyword' not in request.GET and 'group' not in request.GET:
        group = 'Bitmex'
        groupFlag = True

# generate nameList and groupList
    nameList = ['AK','空深空','天乐','trdxz','RoseWhite','colour','REKT','八哥谈币','BitMEX_Jack','神级','落叶风双','Goldman Sachs']
    groupList = ChatLogs.objects.values('group_name').distinct()
    groupList = [i.values()[0] for i in list(groupList) if 'uin' not in i.values()[0]]
    

# Get chat logs from special name
    maxItems = 1000
    data = ChatLogs.objects.exclude(content='')
    if keywordFlag:
        data = data.filter(reduce(operator.and_, [Q(content__icontains=q) for q in split_keyword]))

    if nameFlag:
        data = data.filter(user = name)

    if groupFlag:
        data = data.filter(group_name=group)

    data = data.order_by('-time')[:maxItems]

    return render(request,'chat.html',
            {'cl':data,
            'group_name':groupList,
            'user':nameList})
