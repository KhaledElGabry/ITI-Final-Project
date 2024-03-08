# Generated by Django 5.0.2 on 2024-03-08 19:30

import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=10, validators=[django.core.validators.MinLengthValidator(limit_value=3), django.core.validators.MaxLengthValidator(limit_value=30)])),
                ('last_name', models.CharField(max_length=10, validators=[django.core.validators.MinLengthValidator(limit_value=3), django.core.validators.MaxLengthValidator(limit_value=30)])),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('phone', models.CharField(blank=True, max_length=11, validators=[django.core.validators.RegexValidator(code='invalid_phone', message='Invalid phone number', regex='^01\\d{9}$')])),
                ('usertype', models.CharField(choices=[('customer', 'Customer'), ('vendor', 'Vendor')], null=True)),
                ('address', models.CharField(blank=True, max_length=100)),
                ('shopname', models.CharField(blank=True, max_length=100)),
                ('ssn', models.CharField(max_length=14, null=True, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_ssn', message='SSN must be 14 numeric digits', regex='^[0-9]{14}$')])),
                ('image', models.ImageField(null=True, upload_to='users/images/')),
                ('imageUrl', models.URLField(null=True)),
                ('verification_token', models.CharField(blank=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=False, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
    ]
