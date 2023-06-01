from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from employees.models import Employees
from assets.models import Devices


@login_required
def main_page(request):
    if request.user.groups.filter(name='Admins').exists():
        print('User', request.user.user_name, 'is Admin')
        return redirect("/main/main_page/admins")

    elif request.user.groups.filter(name='Users').exists() and request.user.is_employee:
        print('User', request.user.user_name, 'is User')
        return redirect("/main/main_page/employees")

    else:
        return redirect("/main/main_page/users")


# Є ЗМІНИ:
@login_required
def main_page_employee(request):
    class getdata(object):
        def get_all_employees(self):
            all_employees_data = Employees.objects.all()
            return all_employees_data

        def get_employee_data(self):
            employee_data = Employees.objects.get(user_id=request.user.id)
            return employee_data

        def get_devices_data(self):
            device_data = Devices.objects.filter(user_id=getdata().get_employee_data())
            return device_data

    # ДАНІ КОРИСТУВАЧА:
    user_data = {}
    user_data['u_id'] = request.user.id
    user_data['u_email'] = request.user.email

    # Перевіряємо Admin/Users:
    user_admin = 0
    if request.user.groups.filter(name='Admins').exists():
        user_admin = 1
        user_data['u_group'] = 'Admins'
    else:
        user_data['u_group'] = 'Employees'


    indicate = 'Активний'

    count = len(getdata().get_devices_data())

    return render(request, 'main/_main_page_emp.html', context={
        'page_title': 'Головна сторінка',
        'app_name': '',
        'page_name': 'Головна працівник',
        'user_data': user_data,
        'employee_data': getdata().get_employee_data(),
        'device_data': getdata().get_devices_data(),
        'all_employees_data': getdata().get_all_employees(),
        'count': count,
        'indicate': indicate
    })


# НЕ ЗМІНЮВАТИ
@login_required
def main_page_users(request):
    if not request.user.groups.filter(name='Users').exists():

        return redirect("/")

    else:

        user_data = {}
        user_data['u_id'] = request.user.id
        user_data['u_email'] = request.user.email

        if request.user.groups.filter(name='Users').exists():
            user_data['u_group'] = 'Users'

        if request.user.is_active:
            indicate = 'Активний'
        else:
            indicate = 'Не активний'


        return render(request, 'main/_main_page_user.html', context={
            'page_title': 'Головна сторінка',
            'app_name': '',
            'page_name': 'Головна користувач',
            'user_data': user_data,
            'indicate': indicate,
        })

# НЕ ЗМІНЮВАТИ
@login_required
def main_page_admins(request):
    if request.user.is_employee:
        return redirect("/main/main_page/employees")
    else:
        class getdata(object):
            def get_all_employees(self):
                all_employees_data = Employees.objects.all()
                return all_employees_data

        user_data = {}
        user_data['u_id'] = request.user.id
        user_data['u_email'] = request.user.email

        if request.user.groups.filter(name='Admins').exists():
            user_data['u_group'] = 'Admins'

        if request.user.is_active:
            indicate = 'Активний'
        else:
            indicate = 'Не активний'


        return render(request, 'main/_main_page_admin.html', context={
            'page_title': 'Головна сторінка',
            'app_name': '',
            'page_name': 'Головна адміністратор',
            'user_data': user_data,
            'all_employees_data': getdata().get_all_employees(),
            'indicate': indicate
        })
