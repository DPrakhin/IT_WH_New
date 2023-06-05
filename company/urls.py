from django.urls import path, re_path
from .views import *


urlpatterns = [
    path('news', news, name='company-news'),
    path('details', details, name='details-company'),
    path('create', create, name='create-company'),
    re_path(r'^update/(?P<company_id>[0-9]+)$', update, name='update-company'),
    re_path(r'^delete/(?P<company_id>[0-9]+)$', delete, name='delete-company'),
]
