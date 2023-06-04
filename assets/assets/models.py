from django.db import models
from employees.models import Employees


# ВИРОБНИКИ ОБЛАДНАННЯ:
class Vendors(models.Model):
    vendor = models.CharField(max_length=100, unique=True, default='', verbose_name='Виробник обладнання')
    url = models.URLField(max_length=200, null=True, default='', blank=True, verbose_name='Сайт виробника (URL)')
    vendor_logo = models.FileField(upload_to='vendors/', null=True, blank=True, default='dev_vendor.jpg',
                            verbose_name='Логотип')

    def __str__(self) -> str:
        return str(self.vendor)


# ТИП ОБЛАДНАННЯ:
class DeviceType(models.Model):
    dev_type = models.CharField(max_length=100, unique=True, default='', verbose_name='Тип обладнання')
    dev_type_logo = models.FileField(upload_to='dev_types/', null=True, blank=True, default='dev_type.jpg',
                                     verbose_name='Логотип')

    def __str__(self) -> str:
        return str(self.dev_type)


# СТАТУС ОБЛАДНАННЯ (на складі, у працівника...)
class DeviceStatus(models.Model):
    dev_status = models.CharField(max_length=100, unique=True, default='', verbose_name='Статус обладнання')

    def __str__(self) -> str:
        return str(self.dev_status)


# ГАРАНТІЯ НА ОБЛАДНАННЯ:
class DeviceWarranty(models.Model):
    warranty = models.CharField(max_length=100, unique=True, default='', verbose_name='Термін гарантії')
    comments = models.CharField(max_length=250, default='', null=True, blank=True, verbose_name='Коментарі')

    def __str__(self) -> str:
        return str(self.warranty)


# ПОСТАЧАЛЬНИКИ ОБЛАДНАННЯ:
class Suppliers(models.Model):
    title = models.CharField(max_length=150, unique=True, default='', verbose_name='Назва постачальника')
    url = models.URLField(max_length=200, blank=True, null=True, default='', unique=True,
                          verbose_name='Сайт постачальника (URL)')
    email = models.EmailField(max_length=100, null=True, default='', blank=True, unique=True,
                              verbose_name='Електрона пошта (EMail)')
    phone = models.CharField(max_length=20, default='', null=True, blank=True, verbose_name='Номер телефону')
    comments = models.TextField(max_length=300, default='', null=True, blank=True, verbose_name='Коментарі')

    def __str__(self) -> str:
        return str(self.title)


# ОБЛАДНАННЯ:
class Devices(models.Model):
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE, verbose_name='Тип обладнання')
    device_vendor = models.ForeignKey(Vendors, on_delete=models.CASCADE, verbose_name='Виробник')

    device_title = models.CharField(max_length=250, default='', verbose_name='Назва обладнання')
    device_model = models.CharField(max_length=100, null=True, default='', blank=True, verbose_name='Модель обладнання')
    serial_number = models.CharField(max_length=40, default='No Serial', blank=True, verbose_name='Серійний номер')

    device_status = models.ForeignKey(DeviceStatus, null=True, on_delete=models.SET_NULL,
                                      verbose_name='Статус пристрою')
    user_id = models.ForeignKey(Employees, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Користувач')
    supplier = models.ForeignKey(Suppliers, blank=True, null=True, on_delete=models.SET_NULL,
                                 verbose_name='Постачальник')

    purchase_date = models.DateField(null=True, blank=True, verbose_name='Дата придбання')
    device_warranty = models.ForeignKey(DeviceWarranty, blank=True, null=True, on_delete=models.SET_NULL,
                                        verbose_name='Термін гарантії')
    comments = models.TextField(max_length=500, null=True, default='', blank=True, verbose_name='Коментарі')

    def __str__(self) -> str:
        return str(self.device_type) + ' ' + str(self.device_title)
