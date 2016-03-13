from django.conf.urls import url, include, patterns
from freight.views import *
from freight.models import *

app_name = 'freight'
urlpatterns = [
    # ex: /freight/
    url(r'^$', index, name='index'),
    # ex: /freight/5
    url(r'^(?P<carrier_id>[0-9]+)/$', carrier_detail, name='carrier_detail'),
    # ex: /freight/locations
    url(r'^locations/$', location_all, name='location_all'),
    #ex: /freight/fuel
    url(r'^fuel/$', fuel_surcharge, name='fuel_surcharge'),
    #ex: /freight/history
    url(r'^history/$', rate_history, name='rate_history')
]