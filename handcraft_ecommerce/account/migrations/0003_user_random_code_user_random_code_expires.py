# Generated by Django 5.0.3 on 2024-03-24 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_customtoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='random_code',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='random_code_expires',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
