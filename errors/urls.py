from django.urls import path
from .views import page_403, page_404, login_error

urlpatterns = [
    path("page_403", page_403),
    path("page_404", page_404),
    path("login_error", login_error),
]