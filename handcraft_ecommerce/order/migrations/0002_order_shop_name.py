# Generated by Django 5.0.2 on 2024-03-24 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shop_name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
