from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from django.core.paginator import Paginator
from .forms import *
from django.urls import reverse

# ПЕРЕЛІК ОБЛАДНАННЯ
@login_required
def device_list(request):
    # Базова інформація - для кожної сторінки:
    context = {
        'page_title': 'Список обладнання',
        'app_name': 'Обладнання',
        'page_name': 'Інформація про обладнання'
    }

    # Перевіряємо Admin/Users:
    user_admin = 0
    if request.user.groups.filter(name='Admins').exists():
        user_admin = 1
    if Employees.objects.filter(user_id=request.user.id).exists():
        employee_data = Employees.objects.get(user_id=request.user.id)
    else:
        employee_data = ''
    context['user_admin'] = user_admin
    context['employee_data'] = employee_data
    # ---

    # Pagination:
    if request.method == 'GET':
        pages = 3

        squery = request.GET.get('query')
        if squery == None or squery == '':
            dev_list = Devices.objects.all()
            paginator = Paginator(dev_list, pages)
            page_number = request.GET.get('page')
            page_object = Paginator.get_page(paginator, page_number)
        else:
            incomplete_page = []

            for data in Devices.objects.all():
                list_checker = [str(data.device_type), str(data.device_vendor), str(data.device_title),
                                str(data.device_model), str(data.serial_number), str(data.device_status),
                                str(data.user_id), str(data.supplier), str(data.purchase_date),
                                str(data.device_warranty)]
                get_id = {'id': data.id}
                for output in list_checker:
                    if str(squery) == output:
                        incomplete_page.append(Devices.objects.get(id=get_id.get('id')))

            page_object = []
            [page_object.append(x) for x in incomplete_page if x not in page_object]

    context['dev_list'] = page_object
    return render(request, 'assets/list.html', context=context)


@login_required
def dev_create(request):
    
    context = {
        'page_title': 'Додати обладнання',
        'app_name': 'Обладнання',
        'page_name': 'Додати обладнання'
    }

    if request.user.groups.filter(name='Admins').exists():
        user_admin = 1
    if Employees.objects.filter(user_id=request.user.id).exists():
        employee_data = Employees.objects.get(user_id=request.user.id)
    else:
        employee_data = ''

    context['user_admin'] = user_admin
    context['employee_data'] = employee_data

    if request.method == 'POST':
        form = DevicesForm(request.POST)
        if form.is_valid():
            dev_data = Devices()
            dev_data.device_model = form.cleaned_data['device_model']
            dev_data.device_status = form.cleaned_data['device_status']
            dev_data.device_title = form.cleaned_data['device_title']
            dev_data.device_type = form.cleaned_data['device_type']
            dev_data.device_vendor = form.cleaned_data['device_vendor']
            dev_data.device_warranty = form.cleaned_data['device_warranty']
            dev_data.save()
            return redirect('/assets/list') 
    else:
        form = DevicesForm()
    
    context['form'] = form
    return render(request, 'assets/dev_create.html', context=context)


def device_update(request, device_id=None):
    context = {
        'page_title': 'Оновлення даних',
        'app_name': 'Обладнання',
        'page_name': 'Оновлення даних обладнання'
    }

    user_admin = 0
    if request.user.groups.filter(name='Admins').exists():
        user_admin = 1
    if Employees.objects.filter(user_id=request.user.id).exists():
        employee_data = Employees.objects.get(user_id=request.user.id)
    else:
        employee_data = ''
    context['user_admin'] = user_admin
    context['employee_data'] = employee_data

    if device_id:
        device_info = get_object_or_404(Devices, id=device_id)
    else:
        device_info = None

    form = DevicesForm(instance=device_info)

    if request.method == 'POST':
        form = DevicesForm(request.POST, instance=device_info)
        if form.is_valid():
            form.save()
            return redirect('/assets/list')

    context['device_id'] = device_id
    context['form'] = form
    return render(request, 'assets/device_update.html', context)

def delete_device(request, device_id):
    device = get_object_or_404(Devices, id=device_id)

    user_admin = 0
    if request.user.groups.filter(name='Admins').exists():
        user_admin = 1
    if Employees.objects.filter(user_id=request.user.id).exists():
        employee_data = Employees.objects.get(user_id=request.user.id)
    else:
        employee_data = ''

    if request.method == 'POST':
        device.delete()
        return redirect('/assets/list')

    context = {
        'page_title': 'Видалення обладнання',
        'app_name': 'Обладнання',
        'page_name': 'Видалення обладнання',
        'device': device,
        'device_id': device_id,
        'user_admin': user_admin,
        'employee_data': employee_data
    }
    return render(request, 'assets/device_delete.html', context)


# ПЕРЕЛІК КАТЕГОРІЙ
@login_required
def category(request):
    cat_all = Devices.objects.all()
    d_type = DeviceType.objects.all()
    d_len = len(cat_all)
    #--------- для актуалізації інформації
    if Employees.objects.filter(user_id=request.user.id).exists():
        employee_data = Employees.objects.get(user_id=request.user.id)
    else:
        employee_data = ''

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
            'employee_data': employee_data,
        })

    else:
        # Користувач в группі Users
        user_admin = 0

        return render(request, 'assets/category.html', context={
            'cat': cat_all,
            'user_admin': user_admin,
            'dev_type': d_type,
            'd_len': d_len,
            'employee_data': employee_data,
        })


# ПЕРЕЛІК ВИРОБНИКІВ
@login_required
def vendors(request):
    # Базова інформація - для кожної сторінки:
    context = {
        'page_title': 'Виробники',
        'app_name': 'Обладання',
        'page_name': 'Перелік виробників'
    }

    # Перевіряємо Admin/Users:
    user_admin = 0
    if request.user.groups.filter(name='Admins').exists():
        user_admin = 1
    if Employees.objects.filter(user_id=request.user.id).exists():
        employee_data = Employees.objects.get(user_id=request.user.id)
    else:
        employee_data = ''

    vend_list = []
    all_vendors = Vendors.objects.all()
    for ven_data in all_vendors:
        try:
            devices = Devices.objects.filter(device_vendor=ven_data)
        except Devices.DoesNotExist:
            dev_count = 0
        else:
            dev_count = devices.count()

        our_ven_data = (ven_data, dev_count)
        vend_list.append(our_ven_data)

    context['user_admin'] = user_admin
    context['employee_data'] = employee_data
    context['vend_list'] = vend_list

    return render(request, 'assets/vendors.html', context=context)

def vendor_delete(request, vendor_id):
    vendor = get_object_or_404(Vendors, id=vendor_id)
    count = len(Devices.objects.filter(device_vendor=vendor_id))

    if request.method == 'POST':
        vendor.delete()
        return redirect('/assets/vendors')

    context = {
        'page_title': 'Видалення виробника',
        'app_name': 'Обладання',
        'page_name': 'Видалення виробника',
        'vendor': vendor,
        'count' : count
    }

    return render(request, 'assets/vendor_delete.html', context=context)

@login_required
def vend_create(request):
    
    context = {
        'page_title': 'Додати виробника',
        'app_name': 'Обладнання',
        'page_name': 'Додати виробника'
    }

    if request.user.groups.filter(name='Admins').exists():
        user_admin = 1
    if Employees.objects.filter(user_id=request.user.id).exists():
        employee_data = Employees.objects.get(user_id=request.user.id)
    else:
        employee_data = ''

    context['user_admin'] = user_admin
    context['employee_data'] = employee_data

    if request.method == 'POST':
        form = VendorsForm(request.POST)
        if form.is_valid():
            vend_data = Vendors()
            vend_data.vendor = form.cleaned_data['vendor']
            vend_data.url = form.cleaned_data['url']
            vend_data.vendor_logo = form.cleaned_data['vendor_logo']
            vend_data.save()
            return redirect('/assets/vendors') 
    else:
        form = VendorsForm()
    
    context['form'] = form
    return render(request, 'assets/vend_create.html', context=context)


# ПЕРЕЛІК ПОСТАЧАЛЬНИКІВ
@login_required
def suppliers(request):
    user_admin = 0
    if request.user.groups.filter(name='Admins').exists():
        user_admin = 1
    if Employees.objects.filter(user_id=request.user.id).exists():
        employee_data = Employees.objects.get(user_id=request.user.id)
    else:
        employee_data = ''

    all_s = Suppliers.objects.all()
    num_s = len(all_s)

    return render(request, 'assets/suppliers.html', context={
        'sup': all_s,
        'len_sup': num_s,
        'employee_data': employee_data,
        'user_admin': user_admin,
    })


# ПЕРЕЛІК ГАРАНТІЙ НА ОБЛАДНАННЯ
@login_required
def warranty(request):

    user_admin = 0
    if request.user.groups.filter(name='Admins').exists():
        user_admin = 1
    if Employees.objects.filter(user_id=request.user.id).exists():
        employee_data = Employees.objects.get(user_id=request.user.id)
    else:
        employee_data = ''

    # Завантажуємо дані з бази
    all_devices = Devices.objects.all()
    d_type = DeviceType.objects.all()

    return render(request, 'assets/warranty.html', context={
        'dev': all_devices,
        'dev_type': d_type,
        'user_admin': user_admin,
        'employee_data': employee_data,
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
    if Employees.objects.filter(user_id=request.user.id).exists():
        employee_data = Employees.objects.get(user_id=request.user.id)
    else:
        employee_data = ''
    context['user_admin'] = user_admin
    context['employee_data'] = employee_data
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