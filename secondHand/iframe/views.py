# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
import operator


def iframe(request):
    #return HttpResponse("Hello Django")
    sitename = 'baidu.com'
    return(render(request,'iframe.html',{
        'sn':sitename
        }))
