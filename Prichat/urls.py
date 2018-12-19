# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views_chat, views_word, views_group, views_price

urlpatterns = [
    url(r'^chat$',views_chat.chat,name='chat'),
    url(r'^word$',views_word.word,name='word'),
    url(r'^group$',views_group.group,name='group'),
    url(r'^price$',views_price.price,name='price'),
    url(r'^$',views_group.group,name='group'),
]
