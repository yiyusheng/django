from django.urls import include,path
from . import table 
from django.http import HttpResponse

urlpatterns = [
        path('robots\.txt', lambda r: HttpResponse('User-agent: *\nDisallow: /admin', content_type='text/plain')),
        path('',table.table,name='table'),
]

