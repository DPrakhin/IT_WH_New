from django.urls import path, re_path
from .views import *


urlpatterns = [
    path('list', device_list, name='device-list'),
    path('update/<int:device_id>/', device_update, name='device_update'),
    path('delete/<int:device_id>/', delete_device, name='delete_device'),
    path('dev_create', dev_create, name='dev_create'),
    path('vendors', vendors, name='vendors-list'),
    path('vend_create', vend_create, name='vend_create'),
    path('vendor_delete/<int:vendor_id>/', vendor_delete, name='vendor_delete'),
    path('list', device_list, name='device-list'),
    path('category', category, name='category'),
    path('vendors', vendors, name='vendors-list'),
    path('suppliers', suppliers, name='suppliers-list'),
    path('warranty', warranty, name='warranty-list'),
    path('update_suppliers/<int:supp_id>', sup_update, name='suppliers-update'),
    path('suppliers_delete/<int:supp_id>/', sup_delete, name='suppliers_delete'),
    path('category_create/<int:d_id>', c_create, name='category_create'),
    path('category_delete/<int:d_id>/', c_delete, name='category_delete'),
]
