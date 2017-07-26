# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from show.models import Secondhand
from django.http import HttpResponse

def search(request):
    if request.method == 'GET' and 'keywords' in request.GET and len(request.GET['keywords'])>0:
        rlt = request.GET['keywords']
        item_list = Secondhand.objects.filter(title__contains=rlt).order_by('-create_time')
        if len(item_list)>2000:
            item_list = item_list[:2000]
        #return
        return(render(request,'search.html',
            {'item_list':item_list,
             'len_list': len(item_list)}))
    else:
        #return render(request,'search.html')
        return redirect('show')
        #pass
