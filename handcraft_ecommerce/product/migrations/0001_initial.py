# Generated by Django 5.0.2 on 2024-03-12 19:39

import datetime
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cateName', models.CharField(max_length=50, verbose_name='Category Name')),
                ('cateDescription', models.CharField(blank=True, default='', max_length=250, verbose_name='Category Description')),
                ('cateImage', models.ImageField(upload_to='category/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])], verbose_name='Category Image')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prodName', models.CharField(max_length=100, verbose_name='Product Title')),
                ('prodPrice', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Product Price')),
                ('prodDescription', models.TextField(blank=True, default='', max_length=450, null=True, verbose_name='Product Description')),
                ('prodOnSale', models.BooleanField(default=False, verbose_name='On Sale')),
                ('prodStock', models.IntegerField(default=0, verbose_name='On Stock')),
                ('prodImageThumbnail', models.ImageField(blank=True, default='thumbnails/no-product.png', null=True, upload_to='product/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])], verbose_name='Image Thumbnail')),
                ('prodImageUrl', models.URLField(null=True)),
                ('prodFavorite', models.ManyToManyField(blank=True, related_name='Favorite', to=settings.AUTH_USER_MODEL, verbose_name='favorite')),
                ('prodVendor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prodImages', models.FileField(upload_to='product/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])], verbose_name='Product Images')),
                ('prodImgsForProduct', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='product.product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Product Image',
                'verbose_name_plural': 'Product Images',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rateRating', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0, 'Rating must be at least 0.0'), django.core.validators.MaxValueValidator(5.0, 'Rating cannot exceed 5.0')], verbose_name='Rate')),
                ('rateSubject', models.CharField(max_length=2000)),
                ('rateReview', models.TextField(blank=True, max_length=2000)),
                ('rateCreatedDate', models.DateTimeField(default=datetime.datetime.now)),
                ('rateCustomer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('rateProduct', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subCateName', models.CharField(max_length=50, verbose_name='Sub Category Name')),
                ('subCateDescription', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='Sub Category Description')),
                ('subCateImage', models.ImageField(blank=True, upload_to='subCategory/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])], verbose_name='Sub Category Image')),
                ('subCateParent', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='product.category', verbose_name='General Category')),
            ],
            options={
                'verbose_name': 'Sub Category',
                'verbose_name_plural': 'Sub Categories',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='prodSubCategory',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='product.subcategory', verbose_name='Sub Category Name'),
        ),
    ]
