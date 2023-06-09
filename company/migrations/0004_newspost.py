# Generated by Django 4.2.1 on 2023-06-05 12:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0012_alter_employees_photo'),
        ('company', '0003_alter_company_company_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_heading', models.CharField(default='', max_length=200, verbose_name='Заголовок *')),
                ('description', models.TextField(blank=True, default='', max_length=650, null=True, verbose_name='Опис *')),
                ('post_image', models.FileField(blank=True, default='default-post.jpg', null=True, upload_to='posts/', verbose_name='Фото')),
                ('post_date', models.DateField(blank=True, null=True, verbose_name='Дата завантаження')),
                ('tag', models.CharField(default='', max_length=150, verbose_name='Тег *')),
                ('author', models.ForeignKey(blank=True, help_text='Оберіть автора', null=True, on_delete=django.db.models.deletion.SET_NULL, to='employees.employees', verbose_name='Автор')),
            ],
        ),
    ]
