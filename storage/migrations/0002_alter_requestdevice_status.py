# Generated by Django 4.1.7 on 2023-06-01 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("storage", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="requestdevice",
            name="status",
            field=models.CharField(
                default="У очікуванні завершення", max_length=120, verbose_name="Статус"
            ),
        ),
    ]