from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.models import Group

from .models import Employees, Departments, UserStatus, Cities
from .forms import CitiesForm, DepartmentsForm, UserStatusForm, EmployeesForm, EmployeesUpdateForm

from users.models import NewUser
from company.models import Company
from assets.models import Devices


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
    try:
        employee_info = Employees.objects.get(email=request.user.email)
    except:
        employee_info = None

    devices_count = 0
    if employee_info:
        if Devices.objects.filter(user_id=employee_info.id):
            devices_count = len(Devices.objects.filter(user_id=employee_info.id))

    context['employee_info'] = employee_info
    context['employee_data'] = employee_info
    context['devices_count'] = devices_count
    context['user_admin'] = user_admin
    return render(request, 'employees/about.html', context=context)


@login_required
def emp_list(request):
    # Базова інформація - для кожної сторінки:
    context = {
        'page_title': 'Список співробітників',
        'app_name': 'Співробітники',
        'page_name': 'Інформація про співробітників'
    }

    # Перевіряємо Admin/Users:
    user_admin = 0
    if request.user.groups.filter(name='Admins').exists():
        user_admin = 1
    context['user_admin'] = user_admin
    # ---

    # Pagination:
    employee_list = Employees.objects.all()

    paginator = Paginator(employee_list, 5)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)

    context['employee_list'] = page_object
    return render(request, 'employees/list.html', context=context)


@login_required
def emp_create(request):
    # Базова інформація - для кожної сторінки:
    context = {
        'page_title': 'Додати співробітника',
        'app_name': 'Співробітники',
        'page_name': 'Додати співробітника'
    }

    # Перевіряємо Admin/Users:
    user_admin = 0
    if request.user.groups.filter(name='Admins').exists():
        user_admin = 1

    context['user_admin'] = user_admin
    # ---

    # Починаємо роботу з додавання Співробітника:
    form = EmployeesForm()

    # Як дізнатися про усю інформацію по групах:
    all_groups = Group.objects.all()
    for user_group in all_groups:
        print('GROUP=', user_group.id)
        print('GROUP=', user_group.name)

    # Перевіряємо GET/POST:
    if request.method == 'POST':
        # Важливі дані:
        # group_id == 2 --- Users
        employee_group_id = 2
        employee_password = 'Secret1!'

        # Дані потрібні для відправки листа:
        email_from = 'it.warehouse@itwh.ua'
        email_subject = 'IT.WareHouse: Запис створено'

        form = EmployeesForm(request.POST, request.FILES)
        # Перевіряємо введені дані:
        if form.is_valid():
            employee_data = Employees()

            employee_email = form.cleaned_data['email']
            employee_eid = form.cleaned_data['eid']
            employee_fname = form.cleaned_data['first_name']
            employee_lname = form.cleaned_data['last_name']

            # Перевіряємо, чи є вже такий EMail у базі користувачів:
            try:
                NewUser.objects.get(email=employee_email)

            except:
                # Користувача не знайдено, потрібно створити:
                print('User is not present, will be created')
                new_user = NewUser.objects.create_user(employee_email, employee_fname, employee_password)
                new_user.groups.set([employee_group_id])
                new_user.is_active = True
                new_user.is_employee = True
                new_user.save()
                employee_user_id = new_user.id

                print('User was created, his ID:', employee_user_id)
                email_body = '''
                    <h2>Повідомлення з сайту IT.WareHouse</h2>
                    <hr />
                    <h4 style="color: darkblue;">
                    <h4>Вам створено обліковий запис:</h4>
                    <h4>
                '''

                email_body += 'Логін: ' + employee_email
                email_body += 'Пароль: ' + employee_password

                email_body += '</h4><hr />'

            else:
                employee_user = NewUser.objects.get(email=employee_email)
                employee_user_id = employee_user.id
                employee_user.is_active = True
                employee_user.is_employee = True
                employee_user.save()

                print('User is present, his ID:', employee_user_id)
                email_body = '''
                    <h2>Повідомлення з сайту IT.WareHouse</h2>
                    <hr />
                    <h4 style="color: darkblue;">
                    <h4>Для вас створено запис в базі співробітників:</h4>
                    <hr />
                '''

            # Додаємо користувача у базу даних:
            employee_data.first_name = employee_fname
            employee_data.last_name = employee_lname
            employee_data.email = employee_email
            employee_data.eid = employee_eid
            employee_data.department  = form.cleaned_data['department']
            employee_data.title = form.cleaned_data['title']
            employee_data.user_id = NewUser.objects.get(id=employee_user_id)

            if request.POST.get('photo') == '':
                employee_data.photo = 'photos/default_user.jpg'

            employee_data.mobilephone = form.cleaned_data['mobilephone']
            employee_data.comments = form.cleaned_data['comments']

            city_id = request.POST.get('location')
            if city_id != '':
                employee_data.location = Cities.objects.get(id=city_id)

            ustatus_id = request.POST.get('status')
            if ustatus_id != '':
                employee_data.status = UserStatus.objects.get(id=ustatus_id)

            employee_data.save()

            # Надсилаємо листа користувачу про створення акаунту:
            success = send_mail(email_subject, '', email_from, [employee_email],
                                fail_silently=False, html_message=email_body)
            if success:
                return redirect('/employees/list')

    context['form'] = form
    return render(request, 'employees/emp_create.html', context=context)


@login_required
def emp_details(request, emp_id):
    # Базова інформація - для кожної сторінки:
    context = {
        'page_title': 'Деталі співробітника',
        'app_name': 'Співробітники',
        'page_name': 'Інформація про співробітника'
    }

    # Перевіряємо Admin/Users:
    user_admin = 0
    if request.user.groups.filter(name='Admins').exists():
        user_admin = 1
    context['user_admin'] = user_admin
    # ---

    # 1. Зберігаємо інформацію про потрібного користувача:
    employee_info = Employees.objects.get(id=emp_id)

    # 2. Рахуємо кількість обладнання:
    try:
        len(Devices.objects.filter(user_id=emp_id))
    except:
        devices_count = 0
    else:
        devices_count = len(Devices.objects.filter(user_id=emp_id))

    # 3. Перевіряємо, чи є користувач ProductOwner:
    is_product_owner = 0
    if len(Company.objects.all()) > 0:
        for company in Company.objects.all():
            if company.product_owner is not None:
                if company.product_owner.id == int(emp_id):
                    is_product_owner = 1

    context['employee_info'] = employee_info
    context['devices_count'] = devices_count
    context['is_product_owner'] = is_product_owner
    return render(request, 'employees/emp_details.html', context=context)


@login_required
def emp_update(request, emp_id):
    # Базова інформація - для кожної сторінки:
    context = {
        'page_title': 'Оновлення даних',
        'app_name': 'Співробітники',
        'page_name': 'Оновлення даних співробітника'
    }

    # Перевіряємо Admin/Users:
    user_admin = 0
    if request.user.groups.filter(name='Admins').exists():
        user_admin = 1
    context['user_admin'] = user_admin
    # ---

    # 1. Збираємо потрібну інформацію:
    employee_info = Employees.objects.get(id=emp_id)
    employee_email = employee_info.email
    employee_eid = employee_info.eid

    # 2. Готуємо базову форму:
    form = EmployeesUpdateForm(instance=employee_info)

    # 3. POST or GET:
    if request.method == 'POST':
        form = EmployeesUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            employee_info.first_name = form.cleaned_data['first_name']
            employee_info.last_name = form.cleaned_data['last_name']
            employee_info.mobilephone = form.cleaned_data['mobilephone']
            employee_info.comments = form.cleaned_data['comments']
            employee_info.department = form.cleaned_data['department']
            employee_info.title = form.cleaned_data['title']

            if request.POST.get('photo') == '':
                employee_info.photo = 'photos/default_user.jpg'

            city_id = request.POST.get('location')
            if city_id != '':
                employee_info.location = Cities.objects.get(id=city_id)
            else:
                employee_info.location = None

            ustatus_id = request.POST.get('status')
            if ustatus_id != '':
                employee_info.status = UserStatus.objects.get(id=ustatus_id)
            else:
                employee_info.status = None

            employee_info.save()
            return redirect('/main/main_page')

    context['employee_email'] = employee_email
    context['employee_eid'] = employee_eid
    context['employee_id'] = emp_id
    context['form'] = form
    return render(request, 'employees/emp_update.html', context=context)


@login_required
def emp_delete(request, emp_id):
    # Базова інформація - для кожної сторінки:
    context = {
        'page_title': 'Видалити',
        'app_name': 'Співробітники',
        'page_name': 'Видалити співробітника'
    }

    # Перевіряємо Admin/Users:
    user_admin = 0
    if request.user.groups.filter(name='Admins').exists():
        user_admin = 1
    context['user_admin'] = user_admin
    # ---

    # 1. Базова інформація про співробітника:
    employee_info = Employees.objects.get(id=emp_id)

    # 2. Кількість обладнання у співробітника:
    if Devices.objects.filter(user_id=emp_id):
        devices_count = len(Devices.objects.filter(user_id=emp_id))
    else:
        devices_count = 0

    # 3. Перевіряємо, чи є product_owner
    #    визначаємо його ID:
    product_owner = -1
    product_owner_email = None

    if Company.objects.all():
        for company in Company.objects.all():
            if company.product_owner:
                if company.product_owner.id == int(emp_id):
                    product_owner = company.product_owner.id
                    product_owner_email = Employees.objects.get(id=product_owner).email
                    product_owner = -10
                else:
                    product_owner = company.product_owner.id
                    product_owner_email = Employees.objects.get(id=product_owner).email

    # 4. Шукаємо користувача пов'язаного зі співробітником:
    user_employee_id = None
    if NewUser.objects.filter(email=employee_info.email):
        user_employee_id = NewUser.objects.get(email=employee_info.email).id

    # 5. Робимо перевірку, чи може бути співробітник видалений із бази:
    if request.user.email == employee_info.email:
        # Користувач не може видалити сам себе:
        can_delete = -1
    elif product_owner == -1 and devices_count == 0:
        can_delete = 1
    elif product_owner >= 0:
        can_delete = 10
    else:
        can_delete = -1

    # Подальша обробка:
    if request.method == 'POST':
        # Видалення - простий випадок:
        if can_delete == 1:
            employee_info.delete()
            user_account = NewUser.objects.get(id=user_employee_id)
            user_account.is_employee = False
            user_account.is_staff = False
            user_account.is_active = False
            user_account.save()

        # Видалення, більш складний випадок:
        elif can_delete == 10:
            if devices_count > 0:
                # Потрібно переписати усі пристрої на матеріально-відповідальну особу:
                all_devices = Devices.objects.filter(user_id=emp_id)
                for device in all_devices:
                    device.user_id = Employees.objects.get(email=product_owner_email)
                    device.save()

            employee_info.delete()
            user_account = NewUser.objects.get(id=user_employee_id)
            user_account.is_employee = False
            user_account.is_staff = False
            user_account.is_active = False
            user_account.save()

        return redirect('/employees/list')

    #context['product_owner'] = product_owner
    context['employee_id'] = emp_id
    context['employee_info'] = employee_info
    context['devices_count'] = devices_count
    context['product_owner'] = product_owner
    context['product_owner_email'] = product_owner_email
    context['can_delete'] = can_delete
    return render(request, 'employees/emp_delete.html', context=context)


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
                Employees.objects.filter(department=dep_data.id)
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
                Employees.objects.filter(status=u_status.id)
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
                Employees.objects.filter(location=our_city.id)
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
        'page_title': 'Форма роботи',
        'app_name': 'Співробітники',
        'page_name': 'Додати форму роботи'
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
    # Базова інформація - для кожної сторінки:
    context = {
        'page_title': 'Видалити Відділ',
        'app_name': 'Співробітники',
        'page_name': 'Видалити назву відділу'
    }

    # Перевіряємо Admin/Users:
    user_admin = 0
    if request.user.groups.filter(name='Admins').exists():
        user_admin = 1

    context['user_admin'] = user_admin

    # Збираємо необхідні відомості
    # про кількість співробітників пов'язаних в відділом:
    try:
        Employees.objects.filter(department=dep_id)
    except:
        emp_count = 0
    else:
        emp_count = len(Employees.objects.filter(department=dep_id))


    # Інформацію про сам департмент:
    dep_info = Departments.objects.get(id=dep_id)

    # Перевіряємо GET/POST:
    if request.method == 'POST':
        dep_info.delete()

        return redirect('/employees/departments')

    context['emp_count'] = emp_count
    context['dep_info'] = dep_info
    return render(request, 'employees/deps_delete.html', context=context)


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
    # Базова інформація - для кожної сторінки:
    context = {
        'page_title': 'Видалити форму роботи',
        'app_name': 'Співробітники',
        'page_name': 'Видалити форму роботи'
    }

    # Перевіряємо Admin/Users:
    user_admin = 0
    if request.user.groups.filter(name='Admins').exists():
        user_admin = 1

    context['user_admin'] = user_admin

    # Збираємо необхідні відомості
    # про кількість співробітників пов'язаних з даною формою роботи:
    try:
        Employees.objects.filter(status=ustatus_id)
    except:
        emp_count = 0
    else:
        emp_count = len(Employees.objects.filter(status=ustatus_id))


    # Інформацію про сам департмент:
    ustatus_info = UserStatus.objects.get(id=ustatus_id)

    # Перевіряємо GET/POST:
    if request.method == 'POST':
        ustatus_info.delete()

        return redirect('/employees/ustatus')

    context['emp_count'] = emp_count
    context['ustatus_info'] = ustatus_info
    return render(request, 'employees/ustatus_delete.html', context=context)
