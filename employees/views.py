from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group

from .models import Employees, Departments, UserStatus, Cities
from .forms import CitiesForm, DepartmentsForm, UserStatusForm, EmployeesForm
from users.models import NewUser
from company.models import Company


# ІНФОРМАЦІЯ ПРО ОКРЕМОГО КОРИСТУВАЧА СПІВРОБІТНИКА:
@login_required
def emp_about(request):
    # Базова інформація - для кожної сторінки:
    context = {
        'page_title': 'Мої Дані',
        'app_name': 'Співробітники',
        'page_name': 'Інформація про співробітника'
    }

    # Перевіряємо Admin/Users:
    user_admin = 0
    if request.user.groups.filter(name='Admins').exists():
        user_admin = 1

    # Отримуємо відомості про співробітника з відподвідної бази:
    print('Email = ', request.user.email)
    try:
        employee_info = Employees.objects.get(email=request.user.email)
    except:
        employee_info = None

    context['employee_info'] = employee_info
    context['user_admin'] = user_admin
    return render(request, 'employees/about.html', context=context)


@login_required
def emp_list(request):
    # Базова інформація - для кожної сторінки:
    context = {
        'page_title': 'Мої Дані',
        'app_name': 'Співробітники',
        'page_name': 'Інформація про співробітника'
    }

    # Перевіряємо Admin/Users:
    user_admin = 0
    if request.user.groups.filter(name='Admins').exists():
        user_admin = 1

    if len(Employees.objects.all()) > 0:
        employee_list = Employees.objects.all()

    context['user_admin'] = user_admin
    context['employee_list'] = employee_list
    return render(request, 'employees/list.html', context=context)


@login_required
def emp_create(request):
    # Базова інформація - для кожної сторінки:
    context = {
        'page_title': 'Співробітник',
        'app_name': 'Співробітники',
        'page_name': 'Додати нового співробітника'
    }

    # Перевіряємо Admin/Users:
    user_admin = 0
    if request.user.groups.filter(name='Admins').exists():
        user_admin = 1

    context['user_admin'] = user_admin

    # Починаємо роботу з додавання Співробітника:
    form = EmployeesForm()

    # Як дізнатися про усю інформацію по групах:
    # all_groups = Group.objects.all()
    # for user_group in all_groups:
    #    print('GROUP=', user_group.id)
    #    print('GROUP=', user_group.name)

    # Перевіряємо GET/POST:
    if request.method == 'POST':
        form = EmployeesForm(request.POST, request.FILES)
        user_id = -1
        user_password = 'Secret1!'

        # Перевіряємо введені дані:
        if form.is_valid():
            employee_email = form.cleaned_data['email']
            employee_name = form.cleaned_data['first_name']

            # Перевіряємо, чи є вже такий EMail у базі користувачів:
            try:
                NewUser.objects.get(email=employee_email)

            except:
                # Користувача не знайдено, потрібно створити:
                new_user = NewUser.objects.create_user(employee_email, employee_name, user_password)
                new_user.groups.set([2])
                new_user.is_active = True
                new_user.is_employee = True
                new_user.save()
                print('No users found')

            else:
                user_id = NewUser.objects.get(email=employee_email).id
            # ---

            return redirect('/employees/list')

    context['form'] = form
    return render(request, 'employees/emp_create.html', context=context)


@login_required
def dep_list(request):
    # Базова інформація - для кожної сторінки:
    context = {
        'page_title': 'Відділи',
        'app_name': 'Співробітники',
        'page_name': 'Перелік відділів'
    }

    # Перевіряємо Admin/Users:
    user_admin = 0
    if request.user.groups.filter(name='Admins').exists():
        user_admin = 1

    deps_list = None
    if len(Departments.objects.all()) > 0:
        all_departments = Departments.objects.all()
        deps_list = []

        for dep_data in all_departments:
            # Шукаємо співробітників із данного відділу:
            try:
                Employees.objects.get(department=dep_data.id)
            except:
                emp_count = 0
            else:
                emp_count = len(Employees.objects.filter(department=dep_data.id))

            our_dep_data = (dep_data, emp_count)
            deps_list.append(our_dep_data)

    context['user_admin'] = user_admin
    context['deps_list'] = deps_list
    return render(request, 'employees/dep_list.html', context=context)


@login_required
def ustatus_list(request):
    # Базова інформація - для кожної сторінки:
    context = {
        'page_title': 'Форма роботи',
        'app_name': 'Співробітники',
        'page_name': 'Форма роботи'
    }

    # Перевіряємо Admin/Users:
    user_admin = 0
    if request.user.groups.filter(name='Admins').exists():
        user_admin = 1

    user_status_list = None
    if len(UserStatus.objects.all()) > 0:
        all_user_status = UserStatus.objects.all()
        user_status_list = []

        for u_status in all_user_status:
            # Шукаємо співробітників із данного відділу:
            try:
                Employees.objects.get(status=u_status.id)
            except:
                emp_count = 0
            else:
                emp_count = len(Employees.objects.filter(status=u_status.id))

            our_status_data = (u_status, emp_count)
            user_status_list.append(our_status_data)

    context['user_admin'] = user_admin
    context['ustatus_list'] = user_status_list
    return render(request, 'employees/ustatus_list.html', context=context)


@login_required
def cities_list(request):
    # Базова інформація - для кожної сторінки:
    context = {
        'page_title': 'Наші Локації',
        'app_name': 'Співробітники',
        'page_name': 'Перелік локацій'
    }

    # Перевіряємо Admin/Users:
    user_admin = 0
    if request.user.groups.filter(name='Admins').exists():
        user_admin = 1

    our_city_list = None
    if len(Cities.objects.all()) > 0:
        all_cities = Cities.objects.all()
        our_city_list = []

        for our_city in all_cities:
            # Шукаємо співробітників із даного міста:
            try:
                Employees.objects.get(location=our_city.id)
            except:
                emp_count = 0

            else:
                emp_count = len(Employees.objects.filter(location=our_city.id))

            # Дуже цікавий момент - робимо кортеж, а потім додаємо його до списку:
            data_my = (our_city, emp_count)
            our_city_list.append(data_my)

    print(our_city_list)
    context['user_admin'] = user_admin
    context['cities_list'] = our_city_list
    return render(request, 'employees/cities_list.html', context=context)


@login_required
def dep_create(request):
    # Базова інформація - для кожної сторінки:
    context = {
        'page_title': 'Додати Відділ',
        'app_name': 'Співробітники',
        'page_name': 'Додати відділ компанії'
    }

    # Перевіряємо Admin/Users:
    user_admin = 0
    if request.user.groups.filter(name='Admins').exists():
        user_admin = 1

    # Перевірка GET/POST:
    form = DepartmentsForm()
    if request.method == 'POST':
        form = DepartmentsForm(request.POST)

        if form.is_valid():
            # Якщо форма заповнена - зберігаємо дані:
            dep_data = Departments()
            dep_data.department = form.cleaned_data['department']

            dep_data.save()
            return redirect('/employees/departments')

    context['form'] = form
    context['user_admin'] = user_admin
    return render(request, 'employees/dep_create.html', context=context)


@login_required
def ustatus_create(request):
    # Базова інформація - для кожної сторінки:
    context = {
        'page_title': 'Наші Локації',
        'app_name': 'Співробітники',
        'page_name': 'Перелік локацій'
    }

    # Перевіряємо Admin/Users:
    user_admin = 0
    if request.user.groups.filter(name='Admins').exists():
        user_admin = 1

    # Перевіряємо GET/POST:
    form = UserStatusForm()
    if request.method == 'POST':
        form = UserStatusForm(request.POST)

        if form.is_valid():
            ustatus_data = UserStatus()

            ustatus_data.ustatus = form.cleaned_data['ustatus']
            ustatus_data.save()

            return redirect('/employees/ustatus')

    context['user_admin'] = user_admin
    context['form'] = form
    return render(request, 'employees/ustatus_create.html', context=context)


@login_required
def city_create(request):
    # Базова інформація - для кожної сторінки:
    context = {
        'page_title': 'Додати Локацію',
        'app_name': 'Співробітники',
        'page_name': 'Додати назву локації'
    }

    # Перевіряємо Admin/Users:
    user_admin = 0
    if request.user.groups.filter(name='Admins').exists():
        user_admin = 1

    context['user_admin'] = user_admin

    # Перевірка GET/POST:
    form = CitiesForm()
    if request.method == 'POST':
        form = CitiesForm(request.POST)

        if form.is_valid():
            # Якщо форма заповнена - зберігаємо дані:
            city_data = Cities()
            city_data.city = form.cleaned_data['city']

            city_data.save()
            return redirect('/employees/cities')

    context['form'] = form
    return render(request, 'employees/city_create.html', context=context)


@login_required
def dep_delete(request, dep_id):
    pass


@login_required
def city_delete(request, city_id):
    # Базова інформація - для кожної сторінки:
    context = {
        'page_title': 'Видалити Локацію',
        'app_name': 'Співробітники',
        'page_name': 'Видалити назву локації'
    }

    # Перевіряємо Admin/Users:
    user_admin = 0
    if request.user.groups.filter(name='Admins').exists():
        user_admin = 1

    context['user_admin'] = user_admin

    # Збираємо необхідні відомості:
    # Про кількість співробітників пов'язаних з містом:
    try:
        Employees.objects.filter(location=city_id)
    except:
        emp_count = 0
    else:
        emp_count = len(Employees.objects.filter(location=city_id))

    # Про кількість пов'язаних з містом компаній:
    try:
        Company.objects.filter(city=city_id)
    except:
        company_count = 0
    else:
        company_count = len(Company.objects.filter(city=city_id))

    # Інформацію про саме місто:
    city_info = Cities.objects.get(id=city_id)

    # Перевіряємо GET/POST:
    if request.method == 'POST':
        city_info.delete()

        return redirect('/employees/cities')

    context['emp_count'] = emp_count
    context['company_count'] = company_count
    context['city_info'] = city_info
    return render(request, 'employees/city_delete.html', context=context)


@login_required
def ustatus_delete(request, ustatus_id):
    pass
