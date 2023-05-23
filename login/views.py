from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


# ЛОГІН КОРИСТУВАЧА В СИСТЕМУ:
def index(request):
    # Авторизований користувач завжди потрапляє на головну сторінку:
    if request.user.is_authenticated:
        return redirect('/main/main_page/employees')

    else:
        if request.method == 'POST':
            # Отримуємо необхідні дані:
            request.session.set_expiry(0)
            user_email = request.POST.get('user_email')
            user_password = request.POST.get('user_pass')

            if request.POST.get('keep_logged') == 'on':
                request.session.set_expiry(5 * 24 * 60 * 60)

            # Аутентифікація:
            user = authenticate(request, email=user_email, password=user_password)
            if user and user.is_active:
                # Успішно пройшли аутентифікацію:
                login(request, user)
                return redirect('/main/main_page')

            else:
                return redirect("/errors/login_error")

        else:
            return render(request, 'login/index.html', context={
                'page_title': 'Логін',
                'app_name': '',
                'page_name': 'Вхід до системи'
            })


# ЗАБУЛИ ПАРОЛЬ ?:
# 1. Якщо користувач авторизований - заміна паролю через власний профіль
# 2. Якщо користувач не авторизований - скидання паролю
def forgot_password(request):
    if request.user.is_authenticated:
        return redirect('/users/my_profile')
    else:
        return redirect('/password-reset')


# ВИХІД КОРИСТУВАЧА ІЗ СИСТЕМИ:
def user_logout(request):
    logout(request)
    return redirect("/")


# ФОРМА ЗВОРОТНЬОГО ЗВ'ЯЗКУ:
@login_required
def contact_us(request):
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

    if request.method == 'POST':
        # Отримуємо дані із форми:
        email_user = request.user.user_name
        email_from = request.user.email
        email_subject = request.POST.get('subject')
        email_message = request.POST.get('message')
        email_to = 'it.warehouse@itwh.ua'

        # Невиличка доробка:
        email_subject = 'Повідомлення з сайту: ' + email_subject
        msg_body = '''
            <h2>Повідомлення з сайту IT.WareHouse</h2>
            <hr />
            <h4 style="color: darkblue;">
        '''

        msg_body += 'Користувач: ' + email_user + '\n'
        msg_body += 'Текст повідомлення: '
        msg_body += email_message

        msg_body += '''
            </h4>
            <hr />
        '''

        # Надсилаємо дані через електрону пошту:
        success = send_mail(email_subject, '', email_from, [email_to], fail_silently=False, html_message=msg_body)
        if success:
            return redirect('/main/main_page/employees')

    else:
        context['user_admin'] = user_admin
        return render(request, 'login/contact_us.html', context=context)
