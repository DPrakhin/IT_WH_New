# Generated by Django 4.1.7 on 2023-05-21 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employees", "0002_userstatus_remove_departments_department_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="departments",
            name="dep_title",
            field=models.CharField(
                default="", max_length=100, verbose_name="Назва відділу"
            ),
        ),
    ]
