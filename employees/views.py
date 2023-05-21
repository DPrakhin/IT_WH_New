from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from users.models import NewUser


# ІНФОРМАЦІЯ ПРО ОКРЕМОГО КОРИСТУВАЧА СПІВРОБІТНИКА:
@login_required
def emp_about(request):
    pass


@login_required
def emp_list(request):
    pass


@login_required
def dep_list(request):
    pass


@login_required
def ustatus_list(request):
    pass


@login_required
def cities_list(request):
    pass
