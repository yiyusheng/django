# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from mytest.models import Character
from django.shortcuts import render

def staff1(request):
    staff_list = Character.objects.all()
    staff_str = map(str, staff_list)
    return HttpResponse("<p>"+' '.join(staff_str)+"</p>")

def templay(request):
    context = {}
    context['label'] = 'Hello World!'
    return render(request,'mytest/templay.html',context)

def staff2(request):
    staff_list = Character.objects.all()
    staff_list = map(str,staff_list)
    staff_str = {'label':' '.join(staff_list)}
    return(render(request,'mytest/templay.html',staff_str))

def staff(request):
    staff_list = Character.objects.all()
    return(render(request,'mytest/templay_loop.html',{'staffs':staff_list}))
