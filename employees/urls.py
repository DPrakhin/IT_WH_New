from django.urls import path, re_path
from .views import *


urlpatterns = [
    # Інформація про спвіробітника
    path('about', emp_about, name='employee-about'),
    path('list', emp_list, name='employee-list'),
    path('emp_create', emp_create, name='employee-create'),
    re_path(r'^details/(?P<emp_id>[0-9]+)$', emp_details, name='employee-details'),
    re_path(r'^update/(?P<emp_id>[0-9]+)$', emp_update, name='employee-update'),
    re_path(r'^delete/(?P<emp_id>[0-9]+)$', emp_delete, name='employee-delete'),

    # Інформація про відділи
    path('departments', dep_list, name='department-list'),
    path('dep_create', dep_create, name='department-create'),
    re_path(r'^dep_delete/(?P<dep_id>[0-9]+)$', dep_delete, name='department-delete'),

    # Інформація про форму роботи
    path('ustatus', ustatus_list, name='ustatus-list'),
    path('ustatus_create', ustatus_create, name='ustatus-create'),
    re_path(r'^ustatus_delete/(?P<ustatus_id>[0-9]+)$', ustatus_delete, name='ustatus-delete'),

    # Інформація про локації
    path('cities', cities_list, name='cities-list'),
    path('city_create', city_create, name='cities-create'),
    re_path(r'^city_delete/(?P<city_id>[0-9]+)$', city_delete, name='department-delete'),
]