# -*- coding: utf-8 -*-
from django.urls import include,path
from . import views_chat, views_word, views_price_XBTUSD, views_price_ETHUSD, views_group

urlpatterns = [
    path('chat/',views_chat.chat,name='chat'),
    path('word/',views_word.word,name='word'),
    path('group/',views_group.group,name='group'),
    path('xbtusd/',views_price_XBTUSD.price,name='price_xbtusd'),
    path('ethusd/',views_price_ETHUSD.price,name='price_ethusd'),
    path('',views_group.group,name='group'),
]
