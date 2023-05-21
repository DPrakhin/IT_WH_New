from django.urls import path
from .views import *


urlpatterns = [
    # Інформація про спвіробітника
    path('about', emp_about, name='employee-about'),
    path('list', emp_list, name='employee-list'),

    # Інформація про відділи
    path('departments', dep_list, name='department-list'),

    # Інформація про форму роботи
    path('ustatus', ustatus_list, name='ustatus-list'),

    # Інформація про локації
    path('cities', cities_list, name='cities-list')
]