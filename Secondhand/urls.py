#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Filename: urls.py
#
# Description: 
#
# Copyright (c) 2017, Yusheng Yi <yiyusheng.hust@gmail.com>
#
# Version 1.0
#
# Initial created: 2017-07-13 17:40:01
#
# Last   modified: 2017-07-23 16:19:41
#
#
#
from django.conf.urls import url
from . import web,mobile,word
from django.http import HttpResponse

urlpatterns = [
        url(r'^robots\.txt$', lambda r: HttpResponse('User-agent: *\nDisallow: /admin', content_type='text/plain')),
        url(r'^wordsub/$',word.sub,name='word_sub'),
        url(r'^wordunsub/$',word.unsub,name='word_unsub'),
        url(r'^mobile/$',mobile.secondhand,name='mobile'),
        url(r'^$',web.secondhand,name='secondhand'),
]
