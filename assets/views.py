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
    context['user_admin'] = user_admin
    # ---

    # Pagination:
    dev_list = Devices.objects.all()

    paginator = Paginator(dev_list, 5)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)

    context['dev'] = dev_list
    context['dev_list'] = page_object
    return render(request, 'assets/list.html', context=context)


@login_required
def create_device(request):
    
    context = {
        'page_title': 'Додати обладнання',
        'app_name': 'Обладнання',
        'page_name': 'Додати обладнання'
    }

    if request.user.groups.filter(name='Admins').exists():
        user_admin = 1

    context['user_admin'] = user_admin

    if request.method == 'POST':
        form = DevicesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('assets/list') 
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
    context['user_admin'] = user_admin

    if device_id:
        device_info = get_object_or_404(Devices, id=device_id)
    else:
        device_info = None

    form = DevicesForm(instance=device_info)

    if request.method == 'POST':
        form = DevicesForm(request.POST, instance=device_info)
        if form.is_valid():
            form.save()
            return redirect(reverse('device_update', kwargs={'device_id': device_id}))

    context['id'] = device_id
    context['form'] = form
    return render(request, 'assets/device_update.html', context)

def delete_device(request, device_id):
    device = get_object_or_404(Devices, id=device_id)

    if request.method == 'POST':
        device.delete()
        return redirect('/assets/list')

    context = {
        'page_title': 'Видалення обладнання',
        'app_name': 'Обладнання',
        'page_name': 'Видалення обладнання',
        'device': device,
        'device_id': device_id,
    }
    return render(request, 'assets/device_delete.html', context)


# ПЕРЕЛІК КАТЕГОРІЙ
@login_required
def category(request):
    pass


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
    context['vend_list'] = vend_list

    return render(request, 'assets/vendors.html', context=context)

def vendor_delete(request, vendor_id):
    vendor = get_object_or_404(Vendors, id=vendor_id)

    if request.method == 'POST':
        vendor.delete()
        return redirect('/assets/vendors')

    context = {
        'page_title': 'Видалення виробника',
        'app_name': 'Обладання',
        'page_name': 'Видалення виробника',
        'vendor': vendor
    }

    return render(request, 'assets/vendor_delete.html', context=context)


# ПЕРЕЛІК ПОСТАЧАЛЬНИКІВ
@login_required
def suppliers(request):
    pass


# ПЕРЕЛІК ГАРАНТІЙ НА ОБЛАДНАННЯ
@login_required
def warranty(request):
    pass

