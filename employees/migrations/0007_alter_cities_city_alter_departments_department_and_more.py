# Generated by Django 4.1.7 on 2023-05-21 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employees", "0006_remove_departments_dep_title_departments_department"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cities",
            name="city",
            field=models.CharField(
                max_length=100, unique=True, verbose_name="Назва міста"
            ),
        ),
        migrations.AlterField(
            model_name="departments",
            name="department",
            field=models.CharField(
                max_length=100, unique=True, verbose_name="Назва відділу"
            ),
        ),
        migrations.AlterField(
            model_name="userstatus",
            name="ustatus",
            field=models.CharField(
                max_length=50, unique=True, verbose_name="Форма роботи"
            ),
        ),
    ]
