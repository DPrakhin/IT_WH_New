# Generated by Django 4.1.7 on 2023-05-21 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employees", "0004_alter_departments_dep_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="departments",
            name="dep_title",
            field=models.CharField(
                max_length=100, unique=True, verbose_name="Назва відділу"
            ),
        ),
    ]