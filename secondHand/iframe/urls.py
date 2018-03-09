#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Filename: url.py
#
# Description: 
#
# Copyright (c) 2018, Yusheng Yi <yiyusheng.hust@gmail.com>
#
# Version 1.0
#
# Initial created: 2018-02-26 10:06:36
#
# Last   modified: 2018-02-26 10:08:35
#
#
#
from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.iframe, name='iframe'),
]
