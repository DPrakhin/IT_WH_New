from django.urls import path, re_path
from .views import *


urlpatterns = [
    path('list', device_list, name='device-list'),
    path('update/<int:device_id>/', device_update, name='device_update'),
    path('delete/<int:device_id>/', delete_device, name='delete_device'),
    path('dev_create', create_device, name='create_device'),
    path('category', category, name='category-list'),
    path('vendors', vendors, name='vendors-list'),
    path('vendor_delete/<int:vendor_id>/', vendor_delete, name='vendor_delete'),
    path('suppliers', suppliers, name='suppliers-list'),
    path('warranty', warranty, name='warranty-list')
]
