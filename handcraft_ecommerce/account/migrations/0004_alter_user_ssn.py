# Generated by Django 5.0.2 on 2024-02-29 21:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_user_ssn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='ssn',
            field=models.CharField(max_length=14, null=True, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_ssn', message='SSN must be 14 numeric digits', regex='^[0-9]{14}$')]),
        ),
    ]
