from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from employees.models import Employees
from assets.models import Devices


@login_required
def main_page(request):
    if request.user.groups.filter(name='Admin').exists():
        print('User', request.user.user_name, 'is Admin')
        return redirect("/main/main_page/admins")

    elif request.user.groups.filter(name='Users').exists():
        print('User', request.user.user_name, 'is User')
        return redirect("/main/main_page/users")

    else:
        return redirect("/main/main_page/employees")


# Є ЗМІНИ:
@login_required
def main_page_employee(request):
    # if request.user.groups.filter(name='Users').exists():
    #    return redirect("/")
    # elif request.user.groups.filter(name='Admins').exists() and not request.user.is_employee:
    #    return redirect("/")

    # Якщо користувач авторизований - визначаємо його базові параметри:
    class getdata(object):
        def get_all_employees(self):
            all_employees_data = Employees.objects.all()
            return all_employees_data

        def get_employee_data(self):
            if request.user.is_employee:
                employee_data = Employees.objects.get(user_id=request.user.id)
                return employee_data

        def get_devices_data(self):
            if request.user.is_employee:
                device_data = Devices.objects.filter(user_id=getdata().get_employee_data())
                return device_data

    # ДАНІ КОРИСТУВАЧА:
    user_data = {}
    user_data['u_id'] = request.user.id
    user_data['u_email'] = request.user.email

    #if request.user.is_employee and request.user.groups.filter(name='Admins').exists():
    #    user_data['u_group'] = 'Admins'
    #else:
    #    user_data['u_group'] = 'Employees'
    if request.user.groups.filter(name='Admins').exists():
        user_data['u_group'] = 'Admins'
    else:
        user_data['u_group'] = 'Users'

    # ЯКЩО КОРИСТУВАЧ НЕ АКТИВНИЙ ВІН НЕ МОЖЕ ВОЙТИ ДО СИСТЕМИ:
    # ЦЕ НЕ ПОТРІБНО:
    # if request.user.is_active:
    #        indicate = 'Активний'
    #    else:
    #        indicate = 'Не активний'
    indicate = 'Активний'

    if request.user.is_employee:
        count = len(getdata().get_devices_data())
    else:
        count = ''

    return render(request, 'main/_main_page_emp.html', context={
        'page_title': 'Головна сторінка',
        'app_name': 'Головна',
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
    if not request.user.is_authenticated:
        # Якщо користувач не авторизований - перехід на сторінку авторизації
        return redirect("/")

    elif not request.user.groups.filter(name='Users').exists():

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
            'app_name': 'Головна',
            'page_name': 'Головна користувач',
            'user_data': user_data,
            'indicate': indicate,
        })

# НЕ ЗМІНЮВАТИ
@login_required
def main_page_admins(request):
    if not request.user.is_authenticated:
        # Якщо користувач не авторизований - перехід на сторінку авторизації
        return redirect("/")

    elif request.user.is_employee:

        return redirect("/")

    elif request.user.groups.filter(name='Users').exists():

        return redirect("/")

    else:
        # Якщо користувач авторизований - визначаємо його базові параметри:
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
            'app_name': 'Головна',
            'page_name': 'Головна адміністратор',
            'user_data': user_data,
            'all_employees_data': getdata().get_all_employees(),
            'indicate': indicate
        })


@login_required
def device_update(request, device_id):
    if not request.user.is_authenticated:
        # Якщо користувач не авторизований - перехід на сторінку авторизації
        return redirect("/")
    elif not request.user.is_employee and request.user.groups.filter(name='Admins').exists():

        return redirect("/")

    elif request.user.groups.filter(name='Users').exists():

        return redirect("/")

    elif request.user.is_employee and not request.user.groups.filter(name='Admins').exists():

        return redirect("/")

    else:
        # Обов'язкові відомості про акаунт
        class getdata(object):
            def get_employee_data(self):
                if request.user.groups.filter(name='Admins').exists() and request.user.is_employee:
                    employee_data = Employees.objects.get(user=request.user.id)
                    return employee_data


        user_data = {}
        user_data['u_id'] = request.user.id
        user_data['u_email'] = request.user.email
        if request.user.groups.filter(name='Admins').exists():
            user_data['u_group'] = 'Admins'
        # -----------------


        return render(request, 'main/device_update.html', {
            'page_title': 'Головна сторінка',
            'app_name': 'Обладнання',
            'page_name': 'Редагування',
            'employee_data': getdata().get_employee_data(),
            'user_data': user_data,
        })


@login_required
def device_details(request, device_id):
    if not request.user.is_authenticated:
        # Якщо користувач не авторизований - перехід на сторінку авторизації
        return redirect("/")
    elif not request.user.is_employee and request.user.groups.filter(name='Admins').exists():

        return redirect("/")

    elif request.user.groups.filter(name='Users').exists():

        return redirect("/")

    else:
        # Обов'язкові відомості про акаунт
        class getdata(object):
            def get_employee_data(self):
                if request.user.groups.filter(name='Admins').exists() and request.user.is_employee:
                    employee_data = Employees.objects.get(user=request.user.id)
                    return employee_data
                elif request.user.is_employee:
                    employee_data = Employees.objects.get(user=request.user.id)
                    return employee_data

        user_data = {}
        user_data['u_id'] = request.user.id
        user_data['u_email'] = request.user.email
        if request.user.groups.filter(name='Admins').exists():
            user_data['u_group'] = 'Admins'
        else:
            user_data['u_group'] = 'Employees'
        # -----------------


        return render(request, 'main/device_details.html', {
            'page_title': 'Головна сторінка',
            'app_name': 'Обладнання',
            'page_name': 'Деталі',
            'employee_data': getdata().get_employee_data(),
            'user_data': user_data,
        })


@login_required
def device_delete(request, device_id):
    if not request.user.is_authenticated:
        # Якщо користувач не авторизований - перехід на сторінку авторизації
        return redirect("/")
    elif not request.user.is_employee and request.user.groups.filter(name='Admins').exists():

        return redirect("/")

    elif request.user.groups.filter(name='Users').exists():

        return redirect("/")

    elif request.user.is_employee and not request.user.groups.filter(name='Admins').exists():

        return redirect("/")

    else:
        # Обов'язкові відомості про акаунт
        class getdata(object):
            def get_employee_data(self):
                if request.user.groups.filter(name='Admins').exists() and request.user.is_employee:
                    employee_data = Employees.objects.get(user=request.user.id)
                    return employee_data

        user_data = {}
        user_data['u_id'] = request.user.id
        user_data['u_email'] = request.user.email
        if request.user.groups.filter(name='Admins').exists():
            user_data['u_group'] = 'Admins'

        # -----------------


        return render(request, 'main/device_delete.html', {
            'page_title': 'Головна сторінка',
            'app_name': 'Обладнання',
            'page_name': 'Видалення',
            'employee_data': getdata().get_employee_data(),
            'user_data': user_data,
        })
