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
# Initial created: 2017-07-13 15:18:52
#
# Last   modified: 2017-07-13 16:03:51
#
#
#
from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^staff/',views.staff,name='staff'),
        url(r'^templay/',views.templay,name='templay'),
]
