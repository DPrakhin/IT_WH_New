from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required

from employees.models import Cities, Employees
from .models import Company
from .forms import CompanyForm, CompanyUpdateForm


# Create your views here.
@login_required
def details(request):
    page_title = 'Про Компанію'
    page_name = 'Інформація про Компанію'
    app_name = 'Компанія'
    company_info = {}

    # Перевіряємо, чи є хоча б одна компанія в базі:
    if len(Company.objects.all()) > 0:
        company_count = 1

        for cmp in Company.objects.all():
            company_info = cmp

    else:
        company_count = 0

    # Формуємо дані, які будемо передавати на веб сторінку:
    context = {
        'page_title': page_title,
        'app_name': app_name,
        'page_name': page_name,
        'company_count': company_count,
        'company_info': company_info
    }

    return render(request, 'company/details.html', context=context)


@login_required
def create(request):
    page_title = 'Додати Компанію'
    page_name = 'Додати відомості про компанію'
    app_name = 'Компанія'

    if request.method == 'POST':
        # Cool Test:
        # upd_post = request.POST.copy()
        # print(upd_post)
        # upd_post['company_title'] = 'sss'
        # company_form = CompanyForm(upd_post, request.FILES)

        company_form = CompanyForm(request.POST, request.FILES)

        # Отримуємо необхідні ID:
        city_id = request.POST.get('city')
        boss_id = request.POST.get('company_boss')
        powner_id = request.POST.get('product_owner')

        if company_form.is_valid():
            # Форма заповнена - можемо зберігати:
            company_data = Company()

            company_data.company_logo = company_form.cleaned_data['company_logo']
            company_data.company_title = company_form.cleaned_data['company_title']
            company_data.company_code = company_form.cleaned_data['company_code']

            if city_id != '':
                city = Cities.objects.get(id=city_id)
                company_data.city = city

            company_data.address = company_form.cleaned_data['address']
            company_data.email = company_form.cleaned_data['email']
            company_data.phone = company_form.cleaned_data['phone']

            if boss_id != '':
                boss = Employees.objects.get(id=boss_id)
                company_data.company_boss = boss

            if powner_id != '':
                product_owner = Employees.objects.get(id=powner_id)
                company_data.product_owner = product_owner

            company_data.comments = company_form.cleaned_data['comments']
            company_data.save()

            context = {
                'page_title': page_title,
                'app_name': app_name,
                'page_name': page_name,
                'operation_name': 'Додавання відомостей про компанію в базу',
                'operation_result': 1
            }

            return render(request, 'company/status.html', context=context)

    else:
        # Додатково перевіряємо, чи є компанія в базі:
        if len(Company.objects.all()) > 0:
            return redirect("/company/update")

        else:
            company_form = CompanyForm()

    # Готуємо необхідні дані для сторінки:
    context = {
        'page_title': page_title,
        'app_name': app_name,
        'page_name': page_name,
        'form': company_form,
    }

    return render(request, 'company/create.html', context=context)


@login_required
def update(request, company_id):
    try:
        company_info = Company.objects.get(id=company_id)

    except:
        return redirect('/errors/page_404')

    else:
        page_title = 'Оновити Компанію'
        page_name = 'Оновити відомості про компанію'
        app_name = 'Компанія'

        context = {
            'page_title': page_title,
            'app_name': app_name,
            'page_name': page_name,
            'company_id': company_id
        }

        if request.method == 'POST':
            # upd_post = request.POST.copy()
            # upd_post['company_title'] = str(company_info.company_title)
            # upd_post['company_code'] = str(company_info.company_code)

            # Отримуємо необхідні ID:
            city_id = request.POST.get('city')
            boss_id = request.POST.get('company_boss')
            powner_id = request.POST.get('product_owner')

            #company_form = CompanyUpdateForm(request.POST, request.FILES)
            company_form = CompanyUpdateForm(request.POST, request.FILES)
            if company_form.is_valid():
                # Форма заповнена - можемо зберігати:
                print('We are here #2: ', company_id)

                company_info.company_logo = company_form.cleaned_data['company_logo']
                company_info.address = company_form.cleaned_data['address']
                company_info.email = company_form.cleaned_data['email']
                company_info.phone = company_form.cleaned_data['phone']
                company_info.comments = company_form.cleaned_data['comments']

                if city_id != '':
                    city = Cities.objects.get(id=city_id)
                    company_info.city = city
                else:
                    company_info.city = None

                if boss_id != '':
                    boss = Employees.objects.get(id=boss_id)
                    company_info.company_boss = boss
                else:
                    company_info.company_boss = None

                if powner_id != '':
                    product_owner = Employees.objects.get(id=powner_id)
                    company_info.product_owner = product_owner
                else:
                    company_info.product_owner = None

                company_info.save()

                context = {
                    'page_title': page_title,
                    'app_name': app_name,
                    'page_name': page_name,
                    'company_id': company_id,
                    'operation_name': 'Додавання відомостей про компанію в базу',
                    'operation_result': 1
                }

                return render(request, 'company/status.html', context=context)

        else:
            company_form = CompanyUpdateForm(instance=company_info)

        context['form'] = company_form
    return render(request, 'company/update.html', context=context)


@login_required
def delete(request, company_id):
    try:
        company_info = Company.objects.get(id=company_id)

    except:
        return redirect('/errors/page_404')

    else:
        page_title = 'Видалити Компанію'
        page_name = 'Видалити відомості про компанію'
        app_name = 'Компанія'

        context = {
            'page_title': page_title,
            'app_name': app_name,
            'page_name': page_name,
            'company_id': company_id,
            'company_info': company_info
        }

        if request.method == 'POST':
            company_info.delete()

            context = {
                'page_title': page_title,
                'app_name': app_name,
                'page_name': page_name,
                'operation_name': 'Видалення відомостей про компанію із бази',
                'operation_result': 1
            }

            return render(request, 'company/status.html', context=context)

    return render(request, 'company/delete.html', context=context)


# НОВИНИ КОМПАНІЇ:
@login_required
def news(request):
    pass
