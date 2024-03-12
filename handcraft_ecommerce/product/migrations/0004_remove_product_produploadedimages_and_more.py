# Generated by Django 5.0.2 on 2024-03-12 22:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_remove_product_prodimages_product_produploadedimages'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='prodUploadedImages',
        ),
        migrations.AddField(
            model_name='product',
            name='prodImageFour',
            field=models.ImageField(blank=True, default='thumbnails/no-product.png', null=True, upload_to='product/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])], verbose_name='Product Image Four'),
        ),
        migrations.AddField(
            model_name='product',
            name='prodImageOne',
            field=models.ImageField(blank=True, default='thumbnails/no-product.png', null=True, upload_to='product/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])], verbose_name='Product Image One'),
        ),
        migrations.AddField(
            model_name='product',
            name='prodImageThree',
            field=models.ImageField(blank=True, default='thumbnails/no-product.png', null=True, upload_to='product/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])], verbose_name='Product Image Three'),
        ),
        migrations.AddField(
            model_name='product',
            name='prodImageTwo',
            field=models.ImageField(blank=True, default='thumbnails/no-product.png', null=True, upload_to='product/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])], verbose_name='Product Image Two'),
        ),
    ]
