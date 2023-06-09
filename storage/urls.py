from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', storage, name='storage'),
    path('cart/view', cart_view, name='cart_view'),
    path('cart', cart, name='cart'),
    path('cart_display', cart_display, name='cart_display'),
    path('item_delete', item_delete),
    re_path(r'^cart/view/delete/(?P<item_id>[0-9]+)$', item_wait_delete),
    re_path(r'^cart/view/update/(?P<requests_id>[0-9]+)$', item_update),
    re_path(r'^request_check/(?P<sel_list>[А-Яа-яёЁЇїІіЄєҐґа-щА-ЩЬьЮюЯяЇїІіЄєҐґa-zA-Z0-9!@#$%^&*\,+]{3,})$', request_check),
    re_path(r'^request_confirm/(?P<str_list>[А-Яа-яёЁЇїІіЄєҐґа-щА-ЩЬьЮюЯяЇїІіЄєҐґa-zA-Z0-9!@#$%^&*\,+]{3,})$', request_confirm),
]

