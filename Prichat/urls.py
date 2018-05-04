# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^person$',views.person,name='person'),
    url(r'^word$',views.word,name='word'),
    url(r'^group',views.group,name='group'),
    url(r'',views.group,name='group'),
]
