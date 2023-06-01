from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from employees.models import Employees
from assets.models import Devices
from .forms import EmployeeForm, DeviceForm
from django.contrib.auth.decorators import login_required

# НЕ ЗМІНЮВАТИ
@login_required
def admin_page(request):
    if not request.user.groups.filter(name='Admins').exists():

        return redirect("/")

    else:
        class getdata(object):
            def get_devices_employees(self):
                all_employees_data = Employees.objects.all()
                return all_employees_data

            def get_devices_data(self):
                final_storage = []
                for devices in getdata().get_devices_employees():
                    device_data_all = []
                    inner_data = {}
                    get_data = Devices.objects.filter(user_id=devices)

                    for data in get_data:
                        if data.user_id == devices:
                            local_storage={}
                            local_storage['device_id'] = data.id
                            local_storage['device_type'] = data.device_type
                            local_storage['device_vendor'] = data.device_vendor
                            local_storage['device_title'] = data.device_title
                            local_storage['device_model'] = data.device_model
                            local_storage['serial_number'] = data.serial_number
                            local_storage['device_status'] = data.device_status
                            local_storage['username'] = data.user_id
                            local_storage['supplier'] = data.supplier
                            local_storage['purchase_date'] = data.purchase_date
                            local_storage['device_warranty'] = data.device_warranty
                            local_storage['comments'] = data.comments
                            device_data_all.append(local_storage)
                    inner_data[f'employee'] = devices
                    inner_data['device'] = device_data_all
                    final_storage.append(inner_data)
                return final_storage

            def get_employee_data(self):
                if request.user.groups.filter(name='Admins').exists() and request.user.is_employee:  # поки не використовується
                    employee_data = Employees.objects.get(user_id=request.user.id)
                    return employee_data

        if request.user.groups.filter(name='Admins').exists():
            output = []
            for x in getdata().get_devices_data():
                outer = 0
                for amount in range(len(x.get('device'))+1):
                    outer = amount
                output.append(outer)
            count = sum(output)

        if request.user.groups.filter(name='Admins').exists():
            count_employee = len(getdata().get_devices_employees())


        if request.user.groups.filter(name='Admins').exists():
            user_data = {}
            user_data['u_id'] = request.user.id
            user_data['u_email'] = request.user.email
            if request.user.groups.filter(name='Admins').exists():
                user_data['u_group'] = 'Admins'
            if  request.user.is_active:
                indicate = 'Активний'
            else:
                indicate = 'Не активний'

        if request.method=='GET':
            device_data = []
            pages = 3

            squery = request.GET.get('query')
            if squery == None or squery == '':
                all_data = getdata().get_devices_data()
                paginator = Paginator(all_data, pages)
                page_number = request.GET.get('page')
                device_data = Paginator.get_page(paginator, page_number)
            else:
                for devices in getdata().get_devices_employees():
                    device_data_all = []
                    inner_data = {}
                    get_data = Devices.objects.filter(user_id=devices)

                    if get_data.exists():
                        check = True
                    else:
                        check = False

                    for data in get_data:
                        if data.user_id == devices:
                            list_checker = [str(data.device_type), str(data.device_vendor), str(data.device_title),
                                            str(data.device_model), str(data.serial_number), str(data.device_status),
                                            str(data.user_id), str(data.supplier), str(data.purchase_date), str(data.device_warranty)]
                            for output in list_checker:
                                if str(squery) == output:
                                    sort_check = True
                                    print(devices)
                                    if sort_check == True:
                                        local_storage = {}
                                        local_storage['device_id'] = data.id
                                        local_storage['device_type'] = data.device_type
                                        local_storage['device_vendor'] = data.device_vendor
                                        local_storage['device_title'] = data.device_title
                                        local_storage['device_model'] = data.device_model
                                        local_storage['serial_number'] = data.serial_number
                                        local_storage['device_status'] = data.device_status
                                        local_storage['username'] = data.user_id
                                        local_storage['supplier'] = data.supplier
                                        local_storage['purchase_date'] = data.purchase_date
                                        local_storage['device_warranty'] = data.device_warranty
                                        local_storage['comments'] = data.comments
                                        device_data_all.append(local_storage)

                    entered = False
                    for fir in device_data_all:
                        if fir == []:
                            entered = False
                        else:
                            entered = True

                    if check == True and entered == True:
                        inner_data[f'employee'] = devices
                        inner_data['device'] = device_data_all
                        device_data.append(inner_data)


        return render(request, 'admin_page/index.html', context={
            'page_title': 'Акаунти',
            'app_name': '',
            'page_name': 'Акаунти',
            'user_data': user_data,
            'device_data': device_data,
            'all_employees_data': getdata().get_devices_employees(),
            'employee_data': getdata().get_employee_data(),
            'indicate': indicate,
            'count': count,
            'count_employee': count_employee
        })

# ID відноситься до Devices Table
@login_required
def device_create(request):
    if not request.user.groups.filter(name='Admins').exists():

        return redirect("/")

    else:
        # Обов'язкові відомості про акаунт
        class getdata(object):
            def get_employee_data(self):
                if request.user.groups.filter(name='Admins').exists() and request.user.is_employee:
                    employee_data = Employees.objects.get(user_id=request.user.id)
                    return employee_data

        user_data = {}
        user_data['u_id'] = request.user.id
        user_data['u_email'] = request.user.email
        if request.user.groups.filter(name='Admins').exists():
            user_data['u_group'] = 'Admins'
        # -----------------


        return render(request, 'admin_page/create_device.html', {
            'page_title': 'Обладняння',
            'app_name': 'Головна',
            'page_name': 'Створення',
            'employee_data': getdata().get_employee_data(),
            'user_data': user_data,
        })


@login_required
def device_update(request, deviceinner_device_id):
    if not request.user.groups.filter(name='Admins').exists():

        return redirect("/")

    else:
        # Обов'язкові відомості про акаунт
        class getdata(object):
            def get_employee_data(self):
                if request.user.groups.filter(name='Admins').exists() and request.user.is_employee:
                    employee_data = Employees.objects.get(user_id=request.user.id)
                    return employee_data

        user_data = {}
        user_data['u_id'] = request.user.id
        user_data['u_email'] = request.user.email
        if request.user.groups.filter(name='Admins').exists():
            user_data['u_group'] = 'Admins'

        target_device = Devices.objects.get(id=deviceinner_device_id)

        if request.method == 'GET':
            return render(request, 'admin_page/update_device.html', context={
                'page_title': 'Акаунти',
                'app_name': 'Головна',
                'page_name': 'Оновлення',
                'employee_data': getdata().get_employee_data(),
                'target_post': target_device,
                'form': DeviceForm(instance=target_device),
                'user_data': user_data,
            })
        elif request.method == 'POST':
            form2 = DeviceForm(request.POST)
            if form2.is_valid():
                target_device.device_type = form2.cleaned_data.get('device_type')
                target_device.device_vendor = form2.cleaned_data.get('device_vendor')
                target_device.device_title = form2.cleaned_data.get('device_title')
                target_device.device_model = form2.cleaned_data.get('device_model')
                target_device.serial_number = form2.cleaned_data.get('serial_number')
                target_device.device_status = form2.cleaned_data.get('device_status')
                target_device.user_id = form2.cleaned_data.get('user_id')
                target_device.supplier = form2.cleaned_data.get('supplier')
                target_device.purchase_date = form2.cleaned_data.get('purchase_date')
                target_device.device_warranty = form2.cleaned_data.get('device_warranty')
                target_device.comments = form2.cleaned_data.get('comments')
                target_device.save()
            return redirect('/admin_page/accounts')


@login_required
def device_details(request, deviceinner_device_id):
    if not request.user.groups.filter(name='Admins').exists():

        return redirect("/")

    else:
        # Обов'язкові відомості про акаунт
        class getdata(object):
            def get_employee_data(self):
                if request.user.groups.filter(name='Admins').exists() and request.user.is_employee:
                    employee_data = Employees.objects.get(user_id=request.user.id)
                    return employee_data

        user_data = {}
        user_data['u_id'] = request.user.id
        user_data['u_email'] = request.user.email
        if request.user.groups.filter(name='Admins').exists():
            user_data['u_group'] = 'Admins'
        # -----------------

        devices = Devices.objects.get(id=deviceinner_device_id)

        return render(request, 'admin_page/details_device.html', {
            'page_title': 'Обладняння',
            'app_name': 'Головна',
            'page_name': 'Деталі',
            'employee_data': getdata().get_employee_data(),
            'user_data': user_data,
            'devices': devices
        })


@login_required
def device_delete(request, deviceinner_device_id):
    if not request.user.groups.filter(name='Admins').exists():

        return redirect("/")

    else:
        # Обов'язкові відомості про акаунт
        class getdata(object):
            def get_employee_data(self):
                if request.user.groups.filter(name='Admins').exists() and request.user.is_employee:
                    employee_data = Employees.objects.get(user_id=request.user.id)
                    return employee_data

        user_data = {}
        user_data['u_id'] = request.user.id
        user_data['u_email'] = request.user.email
        if request.user.groups.filter(name='Admins').exists():
            user_data['u_group'] = 'Admins'
        # -----------------

        devices = Devices.objects.get(id=deviceinner_device_id)

        if request.method == 'GET':
            return render(request, 'admin_page/delete_device.html', context={
                'page_title': 'Акаунти',
                'app_name': 'Головна',
                'page_name': 'Видалення',
                'employee_data': getdata().get_employee_data(),
                'user_data': user_data,
                'deviceinner_device': devices
            })
        elif request.method == 'POST':
            devices.delete()

            return redirect('/admin_page/accounts')