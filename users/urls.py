from django.urls import path
from .views import my_profile

urlpatterns = [
    path('my_profile', my_profile)
]