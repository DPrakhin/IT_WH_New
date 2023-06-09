from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone
from employees.models import Employees
from employees.models import Departments
from assets.models import Devices
from users.models import NewUser
from .models import RequestDevice
from .forms import ItemForm
import re
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
import json
@login_required
def storage(request):
    if not request.user.groups.filter(name='Admins').exists():

        return redirect("/")

    else:
        # Обов'язкові відомості про акаунт
        class getdata(object):
            def get_devices_employees(self):
                all_employees_data = Employees.objects.all()
                return all_employees_data

            def get_employee_data(self):
                if request.user.groups.filter(name='Admins').exists() and request.user.is_employee:
                    employee_data = Employees.objects.get(user_id=request.user.id)
                    return employee_data

            def get_devices_data(self):
                final_storage = []
                for devices in getdata().get_devices_employees():
                    device_data_all = []
                    inner_data = {}
                    get_data = Devices.objects.filter(user_id=devices)

                    for data in get_data:
                        get_id = {'id': data.id}
                        if data.user_id == devices:
                            local_storage = Devices.objects.filter(id=get_id.get('id'))
                            device_data_all.append(local_storage)
                    inner_data[f'employee'] = devices
                    inner_data['device'] = device_data_all
                    final_storage.append(inner_data)
                return final_storage

        if request.method == 'GET':
            pages = 3

            squery = request.GET.get('query')
            if squery == None or squery == '':
                all_data = getdata().get_devices_data()
                paginator = Paginator(all_data, pages)
                page_number = request.GET.get('page')
                devices_data = Paginator.get_page(paginator, page_number)
            else:
                devices_data = []
                for devices in getdata().get_devices_employees():
                    device_data_all = []
                    inner_data = {}
                    un_id_storage = []
                    un_id_storage_emp = []
                    get_id_emp = {'id': devices.id}
                    get_data = Devices.objects.filter(user_id=devices)

                    if get_data.exists():
                        check = True
                    else:
                        check = False

                    for data in get_data:
                        if data.user_id == devices:
                            list_checker = [str(data.device_type), str(data.device_vendor), str(data.device_title),
                                            str(data.device_model), str(data.serial_number), str(data.device_status),
                                            str(data.user_id), str(data.supplier), str(data.purchase_date),
                                            str(data.device_warranty)]
                            get_id = {'id': data.id}
                            for output in list_checker:
                                if str(squery) == output:
                                    sort_check = True
                                    if sort_check == True:
                                        un_id_storage.append(get_id.get('id'))

                    list_checker_emp = [str(devices.first_name), str(devices.last_name), str(devices.email),
                                        str(devices.eid), str(devices.title), str(devices.location),
                                        str(devices.mobilephone), str(devices.status)]
                    for output_emp in list_checker_emp:
                        if str(squery) == output_emp:
                            sort_check = True
                            if sort_check == True:
                                check = True
                                un_id_storage_emp.append(get_id_emp.get('id'))
                        elif str(squery) == str(devices.first_name) + ' ' + str(devices.last_name):
                            sort_check = True
                            if sort_check == True:
                                check = True
                                un_id_storage_emp.append(get_id_emp.get('id'))

                    cm_id_storage_emp = []
                    [cm_id_storage_emp.append(x) for x in un_id_storage_emp if x not in cm_id_storage_emp]
                    for indexes in cm_id_storage_emp:
                        device_data_all.append(Devices.objects.filter(user_id=indexes))

                    cm_id_storage = []
                    [cm_id_storage.append(x) for x in un_id_storage if x not in cm_id_storage]
                    for indexes in cm_id_storage:
                        device_data_all.append(Devices.objects.filter(id=indexes))

                    entered = False
                    for fir in device_data_all:
                        if fir == []:
                            entered = False
                        else:
                            entered = True
                    if check == True and entered == True:
                        inner_data[f'employee'] = devices
                        inner_data['device'] = device_data_all
                        devices_data.append(inner_data)

        # ----------- funciton -------------

        item_requests = RequestDevice.objects.all()

        labels_item = []
        data_item_empl_checker = []
        data_item_empl = []

        for item in item_requests:
            data_labels = f'{item.employee.first_name} {item.employee.last_name}'
            labels_item.append(data_labels)
            data_item_empl_checker.append(item.employee)
            data_item_empl.append(item)

        result_item_labels = []
        [result_item_labels.append(x) for x in labels_item if x not in result_item_labels]

        result_item_data = []
        [result_item_data.append(y) for y in data_item_empl_checker if y not in result_item_data]

        get_number = []
        for firstitem in result_item_data:
            number = 0
            for nextitem in data_item_empl:
                if firstitem == nextitem.employee:
                    number += 1
            get_number.append(number)

        # -------------------------------------------------------

        user_data = {}
        user_data['u_id'] = request.user.id
        user_data['u_email'] = request.user.email
        if request.user.groups.filter(name='Admins').exists():
            user_data['u_group'] = 'Admins'

        employee_count = len(getdata().get_devices_employees())

        return render(request, 'storage/index.html', {
            'page_title': 'Склад',
            'app_name': 'Головна',
            'page_name': 'Склад',
            'employee_data': getdata().get_employee_data(),
            'user_data': user_data,
            'devices_data': devices_data,
            'employee_count': employee_count,
            'labels': json.dumps(result_item_labels),
            'data': json.dumps(get_number)
        })
@login_required
def cart_view(request):
    if not request.user.groups.filter(name='Admins').exists():

        return redirect("/")

    else:
        # Обов'язкові відомості про акаунт
        class getdata(object):
            def get_employee_data(self):
                if request.user.groups.filter(name='Admins').exists() and request.user.is_employee:
                    employee_data = Employees.objects.get(user_id=request.user.id)
                    return employee_data

            def get_item_requests(self):
                item_requests = RequestDevice.objects.filter(status='У очікуванні завершення')
                return item_requests

            def get_item_wait(self):
                item_wait = RequestDevice.objects.filter(status='На обробці у відділі')
                return item_wait

        user_data = {}
        user_data['u_id'] = request.user.id
        user_data['u_email'] = request.user.email
        if request.user.groups.filter(name='Admins').exists():
            user_data['u_group'] = 'Admins'

        return render(request, 'storage/cart.html', {
            'page_title': 'Список',
            'app_name': 'Головна',
            'page_name': 'Список',
            'employee_data': getdata().get_employee_data(),
            'user_data': user_data,
            'item_requests': getdata().get_item_requests(),
            'item_wait': getdata().get_item_wait()
        })
@login_required
def request_check(request, sel_list: str):
    if not request.user.groups.filter(name='Admins').exists():

        return redirect("/")

    else:
        # Обов'язкові відомості про акаунт
        class getdata(object):
            def get_employee_data(self):
                if request.user.groups.filter(name='Admins').exists() and request.user.is_employee:
                    employee_data = Employees.objects.get(user_id=request.user.id)
                    return employee_data

        sel_list_str = re.findall(r"[\w']+", sel_list)
        sel_num = [int(x) for x in sel_list_str if x.isdigit()]
        # sel_str = [str(x) for x in sel_list_str if x.isalpha()]
        final_list = []

        for request_id in sel_num:
            request_move = RequestDevice.objects.get(id=request_id)
            final_list.append({
                'product_id': request_move.id,
                'product_code': request_move.code,
                'product_employee': request_move.employee,
                'product_user': request_move.user,
                'product_item': request_move.item,
                'product_status': request_move.status,
                'product_notes': request_move.notes
            })

        user_data = {}
        user_data['u_id'] = request.user.id
        user_data['u_email'] = request.user.email
        if request.user.groups.filter(name='Admins').exists():
            user_data['u_group'] = 'Admins'

        return render(request, 'storage/request_check.html', {
            'page_title': 'Список',
            'app_name': 'Список',
            'page_name': 'Перевірка',
            'employee_data': getdata().get_employee_data(),
            'user_data': user_data,
            'final_list': final_list,
            'str_list': sel_list
        })
@login_required
def request_confirm(request, str_list: str):
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

        if request.method == 'GET':
            return render(request, 'storage/request_confirm.html', {
                'page_title': 'Список',
                'app_name': 'Список',
                'page_name': 'Підтвердження',
                'employee_data': getdata().get_employee_data(),
                'user_data': user_data,
                'str_list': str_list
            })

        elif request.method == 'POST':
            email1 = request.POST.get('email1')
            email2 = request.POST.get('email2')

            sel_list_str = re.findall(r"[\w']+", str_list)
            sel_num = [int(x) for x in sel_list_str if x.isdigit()]
            # sel_str = [str(x) for x in sel_list_str if x.isalpha()]
            final_list = []



            for request_id in sel_num:
                request_move = RequestDevice.objects.get(id=request_id)
                final_list.append({
                    'product_id': request_move.id,
                    'product_code': request_move.code,
                    'product_employee': request_move.employee,
                    'product_user': request_move.user,
                    'product_item': request_move.item,
                    'product_status': request_move.status,
                    'product_notes': request_move.notes
                })

            subject = 'Повідомлення про перелік обладнання для закупівлі'
            body = f"""
                <h1>Повідомлення від Адміна з поштою {email1}</h1>
                <h2 style="color: purple">Замовлення наступних товарів для співробітників</h2>
            """
            for item in final_list:
                body += f"""
                        <hr/>
                        <h3>
                        <p>{item['product_employee']} / {item['product_item']} ** [ {item['product_notes']} ]</p>
                    """
            body += f"""
                        </h3>
                        <hr />
                        <h2>Дякую!</h2>
                    """

            success = send_mail(subject, '', f'{email1}', [email2], fail_silently=False, html_message=body)

            if success:
                for request_id in sel_num:
                    request_dev = RequestDevice.objects.get(id=request_id)
                    request_dev.status = 'На обробці у відділі'
                    request_dev.save()
                return render(request, 'storage/thanks.html', {
                    'page_title': 'Список',
                    'app_name': 'Список',
                    'page_name': 'Успішно',
                    'employee_data': getdata().get_employee_data(),
                    'user_data': user_data,
                })


@login_required
def cart(request):
    response = dict()
    response['test_message'] = 'AJAX works fine!'

    uid = request.GET.get('uid')
    itid = request.GET.get('itid')
    empid = request.GET.get('empid')

    RequestDevice.objects.create(
        code=f'Request-admin/{NewUser.objects.get(id=uid)}/for/{Employees.objects.get(id=empid)}/type/{itid}/{timezone.now()}',
        user_id=uid,
        employee_id=empid,
        item=itid,
        notes=''
    )

    items = RequestDevice.objects.all()
    response['count'] = len(items)

    return JsonResponse(response)
@login_required
def cart_display(request):
    response = dict()
    uid = request.GET.get('uid')
    items = RequestDevice.objects.filter(status='У очікуванні завершення')
    items_wait = RequestDevice.objects.filter(status='На обробці у відділі')

    response['count'] = len(items)
    response['count_wait'] = len(items_wait)

    return JsonResponse(response)
@login_required
def item_update(request, requests_id):
    if not request.user.is_authenticated:
        # Якщо користувач не авторизований - перехід на сторінку авторизації
        return redirect("/")

    elif request.user.groups.filter(name='Users').exists():

        return redirect("/")

    elif not request.user.groups.filter(name='Admins').exists():

        return redirect("/")

    else:
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

        target_device = RequestDevice.objects.get(id=requests_id)
        if request.method == 'GET':
            return render(request, 'storage/update_cart.html', context={
                'page_title': 'Список',
                'app_name': 'Головна',
                'page_name': 'Оновлення',
                'employee_data': getdata().get_employee_data(),
                'target_post': target_device,
                'form': ItemForm(instance=target_device),
                'user_data': user_data,
            })
        elif request.method == 'POST':
            form2 = ItemForm(request.POST)
            if form2.is_valid():
                target_device.user = form2.cleaned_data.get('user')
                target_device.employee = form2.cleaned_data.get('employee')
                target_device.item = form2.cleaned_data.get('item')
                target_device.notes = form2.cleaned_data.get('notes')
                target_device.save()
            return redirect('/storage/cart/view')
@login_required
def item_delete(request):
    response = dict()

    ItemId = request.GET.get('ItemId')
    del_item = RequestDevice.objects.get(id=ItemId)
    del_item.delete()

    response['result'] = 'Запит співробітника був видалений'

    return JsonResponse(response)

@login_required
def item_wait_delete(request, item_id):
    if request.method == 'GET':
        item_wait = RequestDevice.objects.get(id=item_id)
        item_wait.delete()

    return redirect('/storage/cart/view')