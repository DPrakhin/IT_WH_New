# Generated by Django 4.1.7 on 2023-05-23 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("company", "0002_alter_company_address_alter_company_city_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="company_title",
            field=models.CharField(
                default="", max_length=200, verbose_name="Назва компанії *"
            ),
        ),
    ]
