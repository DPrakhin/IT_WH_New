from django import forms
from django.core.exceptions import ValidationError
from .models import Company, NewsPost
from django.utils import timezone
from django.forms import ModelForm
from django.forms.widgets import NumberInput

# ФОРМА КОМПАНІЇ:
class CompanyForm(ModelForm):
    def clean_company_logo(self):
        data = self.cleaned_data['company_logo']

        # Якщо файл не обраний, то додаємо в БД файл за замовчанням:
        if data is None:
            data = 'company/def-logo.jpg'

        else:
            # Якщо файл обраний - перевіряємо його обсяг
            size_limit = 512 * 1024

            if data.size > size_limit:
                raise ValidationError('Увага!! Файл з логотипом компанії повинен бути меньше ніж 512кБ!')

        return data

    # Код ЄДРПОУ - 8 цифр
    def clean_company_code(self):
        data = self.cleaned_data['company_code']

        # Код компанії повинен складатися з 8 символів:
        if len(data) < 8:
            raise ValidationError('Увага!! Код ЄДРПОУ повинен складатися із 8 цифр!')

        # Код компанії повинен складатися лише з цифр:
        if not data.isnumeric():
            raise ValidationError('Увага!! Код ЄДРПОУ повинен складатися лише із цифр!')

        return data

    # Назва компанії - прибираємо зайві пробіли, потрібно хоча б 2 символи:
    def clean_company_title(self):
        data = self.cleaned_data['company_title']
        data = ((data.strip()).lower()).title()

        # Назва компанії більша за 1 символ:
        if len(data) < 2:
            raise ValidationError('Увага!! Назва компанії повинна містити хоча б два символи.')

        return data

    company_logo = forms.FileField(label='Логотип компанії', help_text='Оберіть файл з логотипом компанії (*.jpg)',
                                   allow_empty_file=False, required=False,
                                   widget=forms.FileInput(attrs={'accept': '.jpg'}))
    comments = forms.CharField(label='Коментарі', max_length=300, widget=forms.Textarea, required=False)

    class Meta:
        model = Company
        fields = ['company_title', 'company_code', 'company_logo', 'city', 'address', 'email', 'phone',
                  'company_boss', 'product_owner', 'comments']

        initial = {
            'company_title': '',
            'company_code': '',
            'address': '',
            'email': '',
            'phone': '',
            'comments': ''
        }


class CompanyUpdateForm(ModelForm):
    def clean_company_logo(self):
        data = self.cleaned_data['company_logo']

        # Якщо файл не обраний, то додаємо в БД файл за замовчанням:
        if data is None:
            data = 'company/def-logo.jpg'

        else:
            # Якщо файл обраний - перевіряємо його обсяг
            size_limit = 512 * 1024

            if data.size > size_limit:
                raise ValidationError('Увага!! Файл з логотипом компанії повинен бути меньше ніж 512кБ!')

        return data

    comments = forms.CharField(label='Коментарі', max_length=300, widget=forms.Textarea, required=False)
    company_logo = forms.FileField(label='Логотип компанії', help_text='Оберіть файл з логотипом компанії (*.jpg)',
                                   allow_empty_file=False, required=False,
                                   widget=forms.FileInput(attrs={'accept': '.jpg'}))

    class Meta:
        model = Company
        fields = ['company_title', 'company_logo', 'city', 'address', 'email', 'phone', 'company_boss',
                  'product_owner', 'comments']

class CompanyNews(ModelForm):
    def clean_post_image(self):
        data = self.cleaned_data['post_image']

        # Якщо файл не обраний, то додаємо в БД файл за замовчанням:
        if data is None:
            data = 'posts/default-post.jpg'

        else:
            # Якщо файл обраний - перевіряємо його обсяг
            size_limit = 1920 * 1080

            if data.size > size_limit:
                raise ValidationError('Увага!! Файл з логотипом компанії повинен бути меньше ніж 800кБ!')

        return data

    post_image = forms.FileField(label='Фото', help_text='Оберіть файл (*.jpg)',
                                   allow_empty_file=False, required=False,
                                   widget=forms.FileInput(attrs={'accept': '.jpg'}))
    post_date = forms.DateField(label='Дата завантаження', widget=NumberInput(attrs={'type': 'date'}))
    class Meta:
        model = NewsPost
        fields = ['post_heading', 'description', 'post_image', 'post_date', 'tag', 'author']

        initial = {
            'post_heading': '',
            'description': '',
            'post_date': '',
            'tag': '',
            'author': '',
        }

class UpdateNews(ModelForm):
    def clean_post_image(self):
        data = self.cleaned_data['post_image']

        if data is None:
            data = 'posts/default-post.jpg'

        else:
            size_limit = 1920 * 1080

            if data.size > size_limit:
                raise ValidationError('Увага!! Файл з логотипом компанії повинен бути меньше ніж 800кБ!')

        return data

    post_image = forms.FileField(label='Фото', help_text='Оберіть файл (*.jpg)',
                                   allow_empty_file=False, required=False,
                                   widget=forms.FileInput(attrs={'accept': '.jpg'}))
    class Meta:
        model = NewsPost
        fields = ['post_heading', 'description', 'post_image', 'tag', 'author']
