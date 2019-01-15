# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views_chat, views_word, BMX_XBTUSD, BMX_ETHUSD, views_group

urlpatterns = [
    url(r'^chat/$',views_chat.chat,name='chat'),
    url(r'^word/$',views_word.word,name='word'),
    url(r'^group/$',views_group.group,name='group'),
    url(r'^xbtusd/$',BMX_XBTUSD.price,name='bmx_xbtusd'),
    url(r'^ethusd/$',BMX_ETHUSD.price,name='bmx_ethusd'),
    url(r'^$',views_group.group,name='group'),
]
