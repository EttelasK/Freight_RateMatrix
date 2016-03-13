from django.conf.urls import url

from app.views import *
from app.models import *

#from . import views

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^customer/(?P<c_id>[0-9]+)/$', customer, name='customer'),
    url(r'^wh/(?P<wh_id>[0-9]+)/$', warehouse, name='warehouse'),
    url(r'^customer/new/$',customer_new, name='customer_new')
]