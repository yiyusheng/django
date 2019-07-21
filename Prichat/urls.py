# -*- coding: utf-8 -*-
from django.urls import include,path
from . import views_chat, views_word, views_price_XBTUSD, views_price_ETHUSD, views_group

urlpatterns = [
    path('chat/',views_chat.chat,name='chat'),
    path('word/',views_word.word,name='word'),
    path('group/',views_group.group,name='group'),
    path('data_xbtusd/',views_price_XBTUSD.ChartView.as_view(), name='demo'),
    path('data_ethusd/',views_price_ETHUSD.ChartView.as_view(), name='demo'),
    path('xbtusd/',views_price_XBTUSD.IndexView.as_view(), name='demo'),
    path('ethusd/',views_price_ETHUSD.IndexView.as_view(), name='demo'),
    path('',views_group.group,name='group'),
]
