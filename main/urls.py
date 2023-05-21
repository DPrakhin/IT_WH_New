from django.urls import path
from .views import *


urlpatterns = [
    path('main_page', main_page, name='main_page'),
    path('main_page/admins', main_page_admins, name='admin_main'),
    path('main_page/users', main_page_users, name='user_main'),
    path('main_page/employees', main_page_employee, name='empl_main'),
]