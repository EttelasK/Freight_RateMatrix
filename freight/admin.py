from django.contrib import admin
from freight.models import *

admin.site.register(Carrier)
admin.site.register(Lane)
admin.site.register(LaneRate)
admin.site.register(Location)