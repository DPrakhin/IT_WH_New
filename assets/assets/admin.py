from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(DeviceType)
admin.site.register(DeviceStatus)
admin.site.register(DeviceWarranty)
admin.site.register(Vendors)
admin.site.register(Suppliers)
admin.site.register(Devices)
