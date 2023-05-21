from django.db import models
from users.models import NewUser


# ТАБЛИЦЯ ВІДДІЛІВ:
class Departments(models.Model):
    department = models.CharField(max_length=100, unique=True, verbose_name='Назва відділу')

    def __str__(self) -> str:
        return str(self.department)


# ТАБЛИЦЯ ЛОКАЦІЙ:
class Cities(models.Model):
    city = models.CharField(max_length=100, unique=True, verbose_name='Назва міста')

    def __str__(self) -> str:
        return str(self.city)


# ТАБЛИЦЯ ФОРМИ РОБОТИ (СТАТУС):
class UserStatus(models.Model):
    ustatus = models.CharField(max_length=50, unique=True, verbose_name='Форма роботи')

    def __str__(self) -> str:
        return str(self.ustatus)


# ТАБЛИЦЯ СПІВРОБІТНИКА:
class Employees(models.Model):
    # Обов'язкові поля:
    first_name = models.CharField(max_length=50, default='', verbose_name="Ім'я *")
    last_name = models.CharField(max_length=50, default='', verbose_name='Прізвище *')
    email = models.EmailField(max_length=75, unique=True, null=True, verbose_name='Електрона пошта *')
    eid = models.CharField(max_length=8, unique=True, null=True, verbose_name='Внутрішній номер *')
    department = models.ForeignKey(Departments, null=True, on_delete=models.SET_NULL, verbose_name='Назва відділу *')
    title = models.CharField(max_length=50, null=True, default='', verbose_name='Посада *')
    user_id = models.ForeignKey(NewUser, null=True, on_delete=models.SET_NULL, verbose_name='ID Користувача *')

    # Необов'язкові поля (blank=True):
    location = models.ForeignKey(Cities, null=True, on_delete=models.SET_NULL, blank=True, verbose_name='Назва міста')
    mobilephone = models.CharField(max_length=20, null=True, default='', blank=True, verbose_name='Мобільний телефон')
    status = models.ForeignKey(UserStatus, null=True, on_delete=models.SET_NULL, blank=True,
                               verbose_name='Форма роботи')
    photo = models.FileField(upload_to='photos/', null=True, default='default_user.jpg', blank=True,
                             verbose_name='Фото')
    comments = models.TextField(max_length=300, null=True, default='', blank=True, verbose_name='Коментарі')

    def __str__(self) -> str:
        return str(self.first_name) + '.' + str(self.last_name) + '(email: ' + str(self.email) + ')'

# Just an old data:
#    user = models.OneToOneField(
#        settings.AUTH_USER_MODEL,
#        limit_choices_to={'is_employee': True},
#        on_delete=models.CASCADE
#    )
