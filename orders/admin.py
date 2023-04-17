from django.contrib import admin
from .models import Order, PickupTime, PickupDate

admin.site.register(Order)
admin.site.register(PickupTime)
admin.site.register(PickupDate)