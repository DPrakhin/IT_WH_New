from django import forms
from django.forms import ModelForm
from .models import Cities, Departments, UserStatus, Employees
from django.core.exceptions import ValidationError


# ФОРМА ДЕПАРТАМЕНТІВ:
class DepartmentsForm(ModelForm):
    def clean_dep_title(self):
        data = self.cleaned_data['department']
        data = ((data.strip()).lower()).title()

        if len(data) < 1:
            raise ValidationError('Увага !! Назва відділу не може бути порожня.')

        return data

    class Meta:
        model = Departments
        fields = ['department']

        initial = {
            'department': ''
        }


# ФОРМА ЛОКАЦІЙ:
class CitiesForm(ModelForm):
    def clean_city(self):
        data = self.cleaned_data['city']
        data = ((data.strip()).lower()).title()

        if len(data) < 2:
            raise ValidationError('Увага!! Назва міста повинна складатися хоча б з 2 символів.')

        return data

    class Meta:
        model = Cities
        fields = ['city']

        initial = {
            'city': ''
        }


# ФОРМА ФОРМ РОБОТИ (СТАТУСІВ)
class UserStatusForm(ModelForm):
    def clean_ustatus(self):
        data = self.cleaned_data['ustatus']
        data = ((data.strip()).lower()).title()

        if len(data) < 1:
            raise ValidationError('Увага !! Форма роботи не може бути порожня.')

        return data

    class Meta:
        model = UserStatus
        fields = ['ustatus']

        initial = {
            'ustatus': ''
        }


# ФОРМА СПІВРОБІТНИКА
class EmployeesForm(ModelForm):
    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        data = ((data.strip()).lower()).title()

        if len(data) < 1:
            raise ValidationError('Увага !! Ім"я співробітника не може бути порожнім.')

        return data

    def clean_last_name(self):
        data = self.cleaned_data['last_name']
        data = ((data.strip()).lower()).title()

        if len(data) < 1:
            raise ValidationError('Увага !! Прізвище співробітника не може бути порожнім.')

        return data

    def clean_eid(self):
        data = self.cleaned_data['eid']
        data = (data.strip()).lower()

        if not data.isnumeric():
            raise ValidationError('Увага!! Номер співробітника повинен складатися лише з цифр.')

        if len(data) < 3:
            raise ValidationError('Увага!! Номер співробітника повинен складатися, мінімум, з 3 цифр.')

        return data

    photo = forms.FileField(label='Фото співробітника', help_text='Оберіть файл з фото співробітника (*.jpg)',
                            allow_empty_file=False, required=False, widget=forms.FileInput(attrs={'accept': '.jpg'}))

    class Meta:
        model = Employees
        fields = ['photo', 'first_name', 'last_name', 'email', 'eid', 'department', 'title', 'location', 'mobilephone',
                  'status', 'comments']

        initial = {
            'first_name': '',
            'last_name': '',
            'eid': '',
            'email': '',
            'title': '',
            'mobilephone': '',
            'comments': ''
        }


class EmployeesUpdateForm(ModelForm):
    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        data = ((data.strip()).lower()).title()

        if len(data) < 1:
            raise ValidationError('Увага !! Ім"я співробітника не може бути порожнім.')

        return data

    def clean_last_name(self):
        data = self.cleaned_data['last_name']
        data = ((data.strip()).lower()).title()

        if len(data) < 1:
            raise ValidationError('Увага !! Прізвище співробітника не може бути порожнім.')

        return data

    class Meta:
        model = Employees
        fields = ['photo', 'first_name', 'last_name', 'department', 'title', 'location', 'mobilephone', 'status',
                  'comments']
