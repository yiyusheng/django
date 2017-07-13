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
# Last   modified: 2017-07-13 19:20:18
#
#
#
from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^show/',views.data_display,name='data_display'),
]
