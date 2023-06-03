from django.urls import path, re_path
from .views import *


urlpatterns = [
    path('list', device_list, name='device-list'),
    path('category', category, name='category-list'),
    path('vendors', vendors, name='vendors-list'),
    path('suppliers', suppliers, name='suppliers-list'),
    path('warranty', warranty, name='warranty-list'),

    re_path(r'^update_suppliers/(?P<supp_id>[0-9]+)$', sup_update, name='suppliers-update'),
]
