# -*- coding: utf-8 -*-
from django.urls import include,path
from . import web,word
from django.http import HttpResponse

urlpatterns = [
        path('robots\.txt', lambda r: HttpResponse('User-agent: *\nDisallow: /admin', content_type='text/plain')),
        path('wordsub/',word.sub,name='word_sub'),
        path('wordunsub/',word.unsub,name='word_unsub'),
        path('',web.secondhand,name='secondhand'),
]
