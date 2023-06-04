import datetime
from django import forms
from django.forms import ModelForm, SelectDateWidget
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import *


# СТВОРЕННЯ Й ОПИС ФОРМ:
# ТИП ОБЛАДНАННЯ:
class DeviceTypeForm(ModelForm):
    def clean_dev_type(self):
        data = self.cleaned_data['dev_type']
        data = ((data.strip()).lower()).title()

        if len(data) < 1:
            raise ValidationError('Увага!! Тип обладнання повинен складатися хоча б з одного символу.')

        return data

    dev_type_logo = forms.FileField(label='Логотип', help_text='Оберіть файл з логотипом (*.jpg)',
                                    allow_empty_file=False, required=False,
                                    widget=forms.FileInput(attrs={'accept': '.jpg'}))

    class Meta:
        model = DeviceType
        fields = ['dev_type', 'dev_type_logo']

        initial = {
            'dev_type': ''
        }


# СТАТУС ОБЛАДНАННЯ:
class DeviceStatusForm(ModelForm):
    def clean_dev_status(self):
        data = self.cleaned_data['dev_status']
        data = (data.strip()).upper()

        if len(data) < 1:
            raise ValidationError('Увага!! Статус обладнання повинен складатися хоча б з одного символу.')

        return data

    class Meta:
        model = DeviceStatus
        fields = ['dev_status']

        initial = {
            'dev_status': ''
        }


# ГАРАНТІЯ НА ОБЛАДНАННЯ:
class DeviceWarrantyForm(ModelForm):
    def clean_warranty(self):
        data = self.cleaned_data['warranty']
        data = (data.strip()).lower()

        if len(data) < 1:
            raise ValidationError('Увага!! Гарантія на обладнання повинна складатися хоча б з одного символу.')

        return data

    class Meta:
        model = DeviceWarranty
        fields = ['warranty', 'comments']

        initial = {
            'warranty': '',
            'comments': ''
        }


# ВИРОБНИКИ ОБЛАДНАННЯ:
class VendorsForm(ModelForm):
    def clean_vendor(self):
        data = self.cleaned_data['vendor']
        data = ((data.strip()).lower()).title()

        if len(data) < 1:
            raise ValidationError('Увага!! Назва виробника повинна складатися хоча б з одного символу.')

        return data

    vendor_logo = forms.FileField(label='Логотип', help_text='Оберіть файл з логотипом (*.jpg)',
                           allow_empty_file=False, required=False, widget=forms.FileInput(attrs={'accept': '.jpg'}))

    class Meta:
        model = Vendors
        fields = ['vendor', 'url', 'vendor_logo']

        initial = {
            'vendor': '',
            'url': ''
        }


# ПОСТАЧАЛЬНИКИ:
class SuppliersForm(ModelForm):
    def clean_title(self):
        data = self.cleaned_data['title']
        data = ((data.strip()).lower()).title()

        if len(data) < 1:
            raise ValidationError('Увага!! Назва постачальника повинна складатися хоча б з одного символу.')

        return data

    class Meta:
        model = Suppliers
        fields = ['title', 'url', 'email', 'phone', 'comments']

        initial = {
            'title': '',
            'url': '',
            'email': '',
            'phone': '',
            'comments': ''
        }

def past_year(ago):
    this_year = timezone.now().year
    return list(range(this_year-ago-1, this_year+1))


# ОБЛАДНАННЯ:
class DevicesForm(ModelForm):
    def clean_device_title(self):
        data = self.cleaned_data['device_title']
        data = (data.strip()).lower()

        if len(data) < 1:
            raise ValidationError('Увага!! Назва обладнання повинна складатися хоча б з одного символу.')

        data[0].upper()
        return data
    
    purchase_date = forms.DateField(label='Дата придбання', widget=SelectDateWidget(years=past_year(20)))

    class Meta:
        model = Devices
        fields = ['device_type', 'device_vendor', 'device_title', 'device_model', 'serial_number', 'device_status',
                  'user_id', 'supplier', 'purchase_date', 'device_warranty', 'comments']

        initial = {
            'device_title': '',
            'device_model': '',
            'serial_number': '',
            'purchase_date': datetime.date.today(),
            'comments': ''

        }
