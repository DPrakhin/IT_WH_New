from django.urls import path, re_path
from .views import *


urlpatterns = [
    path('news', news, name='company-news'),
    path('details', details, name='details-company'),
    path('create', create, name='create-company'),
    path('post/create', create_news_post, name='post_create'),
    re_path(r'^update/(?P<company_id>[0-9]+)$', update, name='update-company'),
    re_path(r'^delete/(?P<company_id>[0-9]+)$', delete, name='delete-company'),
    re_path(r'^post/update/(?P<post_id>[0-9]+)$', update_news_post, name='delete-company'),
    re_path(r'^post/delete/(?P<post_id>[0-9]+)$', delete_news_post, name='delete-company'),
]
