# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from Secondhand.models import Secondhand,Advertiser
from datetime import datetime,timedelta
from django.db.models import Max,Q
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from functools import reduce
import operator,re

def table(request):
    print('hello table')
    return render(request,'table.html',{'count':1})
