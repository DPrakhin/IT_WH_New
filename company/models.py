from django.db import models
from employees.models import Cities, Employees


# ОПИС КОМПАНІЇ:
class Company(models.Model):
    # ОБОВ'ЯЗКОВІ ПОЛЯ:
    company_title = models.CharField(max_length=200, unique=True, default='', verbose_name='Назва компанії *')
    company_code = models.CharField(max_length=8, unique=True, default='', verbose_name='Код ЄДРПОУ *')

    # НЕ ОБОВ'ЯЗКОВІ ПОЛЯ:
    company_logo = models.FileField(upload_to='company/', null=True, blank=True, default='def-logo.jpg',
                                    verbose_name='Логотип компанії')

    city = models.ForeignKey(Cities, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Назва міста')
    address = models.CharField(max_length=250, null=True, blank=True, default='', verbose_name='Адреса компанії')
    email = models.EmailField(max_length=100, null=True, blank=True, default='', verbose_name='Електрона пошта')
    phone = models.CharField(max_length=20, null=True, blank=True, default='', verbose_name='Номер телефону')

    company_boss = models.ForeignKey(Employees, related_name='company_boss', null=True, blank=True,
                                     on_delete=models.SET_NULL, verbose_name='Директор компанії',
                                     help_text='Оберіть відповідного співробітника')
    product_owner = models.ForeignKey(Employees, related_name='product_owner', null=True, blank=True,
                                      on_delete=models.SET_NULL, verbose_name='Матеріально-відповідальна особа',
                                      help_text='Оберіть відповідного співробітника')

    comments = models.TextField(max_length=300, default='', null=True, blank=True, verbose_name='Коментарі')


    def __str__(self) -> str:
        return str(self.company_title) + '(ЄДРПОУ: ' + str(self.company_code) + ')'
