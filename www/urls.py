from django.urls import include, path
from . import index

urlpatterns = [
    path('', index.index,name='index'),
    path('secondhand/', include('Secondhand.urls')),
    path('prichat/', include('Prichat.urls')),
]
