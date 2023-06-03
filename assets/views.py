from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Suppliers, Devices, DeviceWarranty, DeviceType
from .forms import SuppliersForm




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
    cat_all = Devices.objects.all()
    d_type = DeviceType.objects.all()
    d_len = len(cat_all)


    # Потрібно визначити групу користувача
    # так як, для Admins та Users різні варіанти:
    if request.user.groups.filter(name='Admin').exists():
        # Користувач в группі Admins
        user_admin = 1

        return render(request, 'assets/category.html', context={
            'cat': cat_all,
            'user_admin': user_admin,
            'dev_type': d_type,
            'd_len': d_len,
        })

    else:
        # Користувач в группі Users
        user_admin = 0

        return render(request, 'assets/category.html', context={
            'cat': cat_all,
            'user_admin': user_admin,
            'dev_type': d_type,
            'd_len': d_len,
        })



# ПЕРЕЛІК ВИРОБНИКІВ
@login_required
def vendors(request):
    pass


# ПЕРЕЛІК ПОСТАЧАЛЬНИКІВ
@login_required
def suppliers(request):
    user_admin = 0
    if request.user.groups.filter(name='Admins').exists():
        user_admin = 1

    all_s = Suppliers.objects.all()
    num_s = len(all_s)

    return render(request, 'assets/suppliers.html', context={
        'sup': all_s,
        'len_sup': num_s,
        'user_admin': user_admin,
    })


# ПЕРЕЛІК ГАРАНТІЙ НА ОБЛАДНАННЯ
@login_required
def warranty(request):

    user_admin = 0
    if request.user.groups.filter(name='Admins').exists():
        user_admin = 1

    # Завантажуємо дані з бази
    all_devices = Devices.objects.all()
    d_type = DeviceType.objects.all()

    return render(request, 'assets/warranty.html', context={
        'dev': all_devices,
        'dev_type': d_type,
        'user_admin': user_admin,
    })




@login_required
def sup_update(request, supp_id):
    # Базова інформація - для кожної сторінки:
    context = {
        'page_title': 'Оновлення даних',
        'app_name': 'Постачальники',
        'page_name': 'Оновлення даних постачальників'
    }

    # Перевіряємо Admin/Users:
    user_admin = 0
    if request.user.groups.filter(name='Admins').exists():
        user_admin = 1
    context['user_admin'] = user_admin
    # ---

    # 1. Збираємо потрібну інформацію:
    suppliers_info = Suppliers.objects.get(id=supp_id)
    suppliers_email = suppliers_info.email
    suppliers_eid = suppliers_info.phone

    # 2. Готуємо базову форму:
    form = SuppliersForm(instance=suppliers_info)

    # 3. POST or GET:
    if request.method == 'POST':
        print('INPUT DATA:', request.POST)

    context['sup_email'] = suppliers_email
    context['sup_eid'] = suppliers_eid
    context['employee_id'] = supp_id
    context['form'] = form
    return render(request, 'assets/update_suppliers.html', context=context)


@login_required
def cc(request):
    if not request.user.groups.filter(name='Admins').exists():

        return redirect("/")

    else:
        # Обов'язкові відомості про акаунт
        class getdata(object):
            def get_employee_data(self):
                if request.user.groups.filter(name='Admins').exists() and request.user.is_employee:
                    employee_data = Devices.objects.get(user_id=request.user.id)
                    return employee_data

        user_data = {}
        user_data['u_id'] = request.user.id
        user_data['u_email'] = request.user.email
        if request.user.groups.filter(name='Admins').exists():
            user_data['u_group'] = 'Admins'
        # -----------------

        return render(request, 'assets/c_c.html', {
            'page_title': 'Обладняння',
            'app_name': 'Головна',
            'page_name': 'Створення',
            'employee_data': getdata().get_employee_data(),
            'user_data': user_data,
        })