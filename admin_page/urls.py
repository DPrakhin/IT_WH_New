from django.urls import path, re_path
from .views import *

# НЕ ЗМІНЮВАТИ
urlpatterns = [
    path('accounts', admin_page, name='accounts'),
    path('accounts/create', user_create, name='user_create'),
    path('devices/create', device_create, name='device_create'),
    re_path(r'^devices/update/(?P<deviceinner_device_id>[0-9]+)$', device_update),
    re_path(r'^devices/details/(?P<deviceinner_device_id>[0-9]+)$', device_details),
    re_path(r'^devices/delete/(?P<deviceinner_device_id>[0-9]+)$', device_delete),
]