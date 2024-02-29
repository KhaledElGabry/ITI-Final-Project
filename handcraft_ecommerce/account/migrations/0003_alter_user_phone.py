# Generated by Django 5.0.2 on 2024-02-29 11:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=11, null=True, validators=[django.core.validators.RegexValidator(code='invalid_phone', message='Invalid phone number', regex='^01\\d{9}$')]),
        ),
    ]
