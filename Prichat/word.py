# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.utils import timezone
from Secondhand.forms import wordSubscribeForm
from Secondhand.models import WordSubscribe
import pymysql

#from datetime import datetime,timedelta
#from Secondhand.models import Secondhand,Advertiser
#from django.db.models import Max,Q
#import operator

def sub(request):
    if request.method == 'POST':
        form = wordSubscribeForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.time = timezone.now()
            post.enable = 1
            post.counts = 0
            post.save()
        return redirect('word_sub')
    else:
        form = wordSubscribeForm()
        ws = WordSubscribe.objects.filter(enable=1)
        return render(request,'wordsub.html',
                {'form':form,
                 'ws':ws,})

def unsub(request):
    if request.method == 'GET' and 'user' in request.GET and 'keyword' in request.GET:
        user = request.GET['user']
        conn = pymysql.connect(host='127.0.0.1',user='root',passwd='qwer1234',db='scrapy',charset='utf8mb4')
        cur = conn.cursor()
        keyword = request.GET['keyword']
        if 'sckey' in request.GET:
            sckey = request.GET['sckey']
            #cur.execute("UPDATE word_subscribe SET enable=0 where sckey=%s and word=%s",
            cur.execute("DELETE FROM word_subscribe WHERE sckey=%s and word=%s",
                    (sckey,keyword))
            rtn = cur.connection.commit()
            return redirect('word_sub')
        else:
            ws = WordSubscribe.objects.filter(enable=1,user=user)
            return render(request,'wordunsub.html',
                    {'user':user,
                     'keyword':keyword,
                     'ws':ws,})
            
    else:
        return redirect('word_sub')
            


