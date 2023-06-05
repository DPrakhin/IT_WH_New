from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required

from employees.models import Cities, Employees
from .models import Company, NewsPost
from .forms import CompanyForm, CompanyUpdateForm, CompanyNews, UpdateNews

import os

# Create your views here.
@login_required
def details(request):
    # Базова інформація - для кожної сторінки:
    context = {
        'page_title': 'Про компанію',
        'app_name': 'Компанія',
        'page_name': 'Інформація про компанію'
    }

    # Перевіряємо Admin/Users:
    user_admin = 0
    if request.user.groups.filter(name='Admins').exists():
        user_admin = 1
    if Employees.objects.filter(user_id=request.user.id).exists():
        employee_data = Employees.objects.get(user_id=request.user.id)
    else:
        employee_data = ''

    # Перевіряємо наявність записів про компанію:
    company_info = None
    if len(Company.objects.all()) > 0:
        company_info = Company.objects.get()

    context['user_admin'] = user_admin
    context['company_info'] = company_info
    context['employee_data'] = employee_data
    return render(request, 'company/details.html', context=context)


@login_required
def create(request):
    # Базова інформація - для кожної сторінки:
    context = {
        'page_title': 'Додати компанію',
        'app_name': 'Компанія',
        'page_name': 'Додати компанію'
    }

    # Перевіряємо Admin/Users:
    user_admin = 0
    if request.user.groups.filter(name='Admins').exists():
        user_admin = 1
    if Employees.objects.filter(user_id=request.user.id).exists():
        employee_data = Employees.objects.get(user_id=request.user.id)
    else:
        employee_data = ''

    # GET/POST:
    if request.method == 'POST':
        # Отримуємо дані із форми:
        city_id = request.POST.get('city')
        boss_id = request.POST.get('company_boss')
        powner_id = request.POST.get('product_owner')

        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            company_data = Company()

            company_data.company_title = form.cleaned_data['company_title']
            company_data.company_code = form.cleaned_data['company_code']
            company_data.address = form.cleaned_data['address']
            company_data.email = form.cleaned_data['email']
            company_data.phone = form.cleaned_data['phone']
            company_data.comments = form.cleaned_data['comments']
            company_data.company_logo = form.cleaned_data['company_logo']

            # Додаткові дані:
            if city_id != '':
                company_data.city = Cities.objects.get(id=city_id)

            if boss_id != '':
                company_data.company_boss = Employees.objects.get(id=boss_id)

            if powner_id != '':
                company_data.product_owner = Employees.objects.get(id=powner_id)

            company_data.save()

            # Успіх => Інформація про компанію:
            return redirect('/company/details')

    else:
        form = CompanyForm()

    context['user_admin'] = user_admin
    context['form'] = form
    context['employee_data'] = employee_data
    return render(request, 'company/create.html', context=context)


@login_required
def update(request, company_id):
    # Базова інформація - для кожної сторінки:
    context = {
        'page_title': 'Оновити компанію',
        'app_name': 'Компанія',
        'page_name': 'Оновити відомості про компанію'
    }

    # Перевіряємо Admin/Users:
    user_admin = 0
    if request.user.groups.filter(name='Admins').exists():
        user_admin = 1
    if Employees.objects.filter(user_id=request.user.id).exists():
        employee_data = Employees.objects.get(user_id=request.user.id)
    else:
        employee_data = ''

    # Отримуємо інформацію про компанію:
    company_info = Company.objects.get(id=company_id)

    # Перевірка GET/POST:
    if request.method == 'POST':
        # Отримуємо дані із форми:
        city_id = request.POST.get('city')
        boss_id = request.POST.get('company_boss')
        powner_id = request.POST.get('product_owner')

        form = CompanyUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            if request.POST.get('post_image') != '':
                company_info.post_image = form.cleaned_data['company_logo']
            company_info.company_title = form.cleaned_data['company_title']
            company_info.address = form.cleaned_data['address']
            company_info.email = form.cleaned_data['email']
            company_info.phone = form.cleaned_data['phone']
            company_info.comments = form.cleaned_data['comments']

            # Додаткові дані:
            if city_id != '':
                company_info.city = Cities.objects.get(id=city_id)
            else:
                company_info.city = None

            if boss_id != '':
                company_info.company_boss = Employees.objects.get(id=boss_id)
            else:
                company_info.company_boss = None

            if powner_id != '':
                company_info.product_owner = Employees.objects.get(id=powner_id)
            else:
                company_info.product_owner = None

            company_info.save()
            return redirect('/company/details')

    else:
        form = CompanyUpdateForm(instance=company_info)

    context['form'] = form
    context['company_info'] = company_info
    context['user_admin'] = user_admin
    context['employee_data'] = employee_data
    return render(request, 'company/update.html', context=context)


@login_required
def delete(request, company_id):
    # Базова інформація - для кожної сторінки:
    context = {
        'page_title': 'Видалити компанію',
        'app_name': 'Компанія',
        'page_name': 'Видалити компанію'
    }

    # Перевіряємо Admin/Users:
    user_admin = 0
    if request.user.groups.filter(name='Admins').exists():
        user_admin = 1
    if Employees.objects.filter(user_id=request.user.id).exists():
        employee_data = Employees.objects.get(user_id=request.user.id)
    else:
        employee_data = ''

    # Отримуємо дані про компанію:
    company_info = Company.objects.get(id=company_id)

    # Якщо усе добре - видаляємо:
    if request.method == 'POST':
        company_info.delete()

        return redirect('/main/main_page')

    context['user_admin'] = user_admin
    context['company_id'] = company_id
    context['company_info'] = company_info
    context['employee_data'] = employee_data
    return render(request, 'company/delete.html', context=context)


# НОВИНИ КОМПАНІЇ:
@login_required
def news(request):
    # Базова інформація - для кожної сторінки:
    context = {
        'page_title': 'Новини компанії',
        'app_name': 'Новини',
        'page_name': 'Усі новини'
    }

    # Перевіряємо Admin/Users:
    user_admin = 0
    if request.user.groups.filter(name='Admins').exists():
        user_admin = 1
    if Employees.objects.filter(user_id=request.user.id).exists():
        employee_data = Employees.objects.get(user_id=request.user.id)
    else:
        employee_data = ''

    news_list = NewsPost.objects.all()
    context['user_admin'] = user_admin
    context['employee_data'] = employee_data
    context['news_list'] = news_list
    return render(request, 'news/details.html', context=context)
@login_required
def create_news_post(request):
    # Базова інформація - для кожної сторінки:
    context = {
        'page_title': 'Додати новину',
        'app_name': 'Новини',
        'page_name': 'Додати новину'
    }

    # Перевіряємо Admin/Users:
    user_admin = 0
    if request.user.groups.filter(name='Admins').exists():
        user_admin = 1
    if Employees.objects.filter(user_id=request.user.id).exists():
        employee_data = Employees.objects.get(user_id=request.user.id)
    else:
        employee_data = ''

    if request.method == 'POST':
        form = CompanyNews(request.POST, request.FILES)
        if form.is_valid():
            post_data = NewsPost()
            post_data.post_heading = form.cleaned_data['post_heading']
            post_data.description = form.cleaned_data['description']
            post_data.post_image = form.cleaned_data['post_image']
            post_data.post_date = form.cleaned_data['post_date']
            post_data.tag = form.cleaned_data['tag']
            post_data.author = form.cleaned_data['author']
            post_data.save()
            return redirect('/company/news')
    else:
        form = CompanyNews()

    context['user_admin'] = user_admin
    context['form'] = form
    context['employee_data'] = employee_data
    return render(request, 'news/news_create.html', context=context)
@login_required
def update_news_post(request, post_id):
    context = {
        'page_title': 'Оновити новину',
        'app_name': 'Новини',
        'page_name': 'Оновити новину'
    }

    user_admin = 0
    if request.user.groups.filter(name='Admins').exists():
        user_admin = 1
    if Employees.objects.filter(user_id=request.user.id).exists():
        employee_data = Employees.objects.get(user_id=request.user.id)
    else:
        employee_data = ''

    news_list = NewsPost.objects.get(id=post_id)

    if request.method == 'POST':
        form = UpdateNews(request.POST, request.FILES)
        if form.is_valid():

            if request.POST.get('post_image') != '':
                news_list.post_image = form.cleaned_data['post_image']
            news_list.post_heading = form.cleaned_data['post_heading']
            news_list.description = form.cleaned_data['description']
            news_list.tag = form.cleaned_data['tag']
            news_list.author = form.cleaned_data['author']
            news_list.save()
            return redirect('/company/news')
        else:
            context = {
                'form': form,
                'news_list': news_list,
                'user_admin': user_admin,
                'employee_data': employee_data,
            }
            return render(request, 'news/news_update.html', context)
    elif request.method == 'GET':
        form = UpdateNews(instance=news_list)

    context['form'] = form
    context['news_list'] = news_list
    context['user_admin'] = user_admin
    context['employee_data'] = employee_data
    return render(request, 'news/news_update.html', context=context)

@login_required
def delete_news_post(request, post_id):
    if request.method == 'GET':
        news_list = NewsPost.objects.get(id=post_id)
        news_list.delete()

    return redirect('/company/news')