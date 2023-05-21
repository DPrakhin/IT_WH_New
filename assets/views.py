from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


# ПЕРЕЛІК ОБЛАДНАННЯ
@login_required
def device_list(request):
    # Потрібно визначити групу користувача
    # так як, для Admins та Users різні варіанти:
    if request.user.groups.filter(name='Admin').exists():
        # Користувач в группі Admins
        pass

    else:
        # Користувач в группі Users
        pass


# ПЕРЕЛІК КАТЕГОРІЙ
@login_required
def category(request):
    # Потрібно визначити групу користувача
    # так як, для Admins та Users різні варіанти:
    if request.user.groups.filter(name='Admin').exists():
        # Користувач в группі Admins
        pass

    else:
        # Користувач в группі Users
        pass


# ПЕРЕЛІК ВИРОБНИКІВ
@login_required
def vendors(request):
    pass


# ПЕРЕЛІК ПОСТАЧАЛЬНИКІВ
@login_required
def suppliers(request):
    pass


# ПЕРЕЛІК ГАРАНТІЙ НА ОБЛАДНАННЯ
@login_required
def warranty(request):
    pass
