from tabnanny import verbose
from tkinter import CASCADE
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from account.models import User
from datetime import datetime
from django.utils import timezone


class Product(models.Model):
    prodVendor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    prodName = models.CharField(max_length=100, verbose_name=('Product Title'))
    prodPrice = models.DecimalField(default=0, decimal_places=2, max_digits=8, verbose_name=('Product Price'))
    prodDescription = models.TextField(max_length=450, default='', blank=True, null=True, verbose_name=('Product Description'))
    prodSubCategory = models.ForeignKey('SubCategory', on_delete=models.CASCADE, default=1, verbose_name=('Sub Category Name'),)
    prodStock = models.IntegerField(default=0, verbose_name=('On Stock'))
    prodOnSale = models.BooleanField(default=False)
    prodImageThumbnail = models.ImageField(upload_to='product/', default='thumbnails/no-product.png', validators=[FileExtensionValidator(['png','jpg','jpeg'])], verbose_name=('Image Thumbnail'), null=True, blank=True)
    prodImageOne = models.ImageField(upload_to='product/', default='thumbnails/no-product.png', validators=[FileExtensionValidator(['png','jpg','jpeg'])], verbose_name=('Product Image One'), null=True, blank=True)
    prodImageTwo = models.ImageField(upload_to='product/', default='thumbnails/no-product.png', validators=[FileExtensionValidator(['png','jpg','jpeg'])], verbose_name=('Product Image Two'), null=True, blank=True)
    prodImageThree = models.ImageField(upload_to='product/', default='thumbnails/no-product.png', validators=[FileExtensionValidator(['png','jpg','jpeg'])], verbose_name=('Product Image Three'), null=True, blank=True)
    prodImageFour = models.ImageField(upload_to='product/', default='thumbnails/no-product.png', validators=[FileExtensionValidator(['png','jpg','jpeg'])], verbose_name=('Product Image Four'), null=True, blank=True)
    prodImageUrl = models.URLField(null=True)
    created_at = models.DateTimeField(default=timezone.now, verbose_name=('Created At'))
    
 
    class Meta:
        verbose_name = ('Product')
        verbose_name_plural = ('Products')

          
        def __str__(self):
          return self.prodName
     
class Rating(models.Model):
    rateProduct=models.ForeignKey(Product, on_delete=models.CASCADE)        
    rateCustomer=models.ForeignKey(User, on_delete=models.CASCADE)
    rateRating=models.FloatField(default=0.0, validators=[MinValueValidator(0.0, "Rating must be at least 0.0"), MaxValueValidator(5.0, "Rating cannot exceed 5.0")], verbose_name=('Rate'))        
    rateSubject=models.CharField(max_length=2000)        
    rateReview=models.TextField(max_length=2000,blank=True)        
    rateCreatedDate=models.DateTimeField(default=datetime.now)    
     


class ProductImage(models.Model):
    prodImgsForProduct = models.ForeignKey(Product, on_delete=models.CASCADE, default=None, verbose_name=('Product'))
    prodImage = models.FileField(upload_to='product/',  validators=[FileExtensionValidator(['png','jpg','jpeg'])], verbose_name=('Product Images'))
    class Meta:
        verbose_name = ("Product Image")
        verbose_name_plural = ("Product Images")

    def __str__(self):
        return str(self.prodImage)



class Category(models.Model):
    cateName = models.CharField(max_length=50, verbose_name=('Category Name'))
    cateDescription = models.CharField(max_length=250, default='', blank=True, verbose_name=('Category Description'))
    cateImage = models.ImageField(upload_to='category/', validators=[FileExtensionValidator(['png','jpg','jpeg'])], verbose_name=('Category Image'))

    class Meta:
        verbose_name = ("Category")
        verbose_name_plural = ("Categories")

    def __str__(self):
        return self.cateName

class SubCategory(models.Model):
    subCateName = models.CharField(max_length=50, verbose_name=('Sub Category Name'))
    subCateParent = models.ForeignKey(Category, on_delete=models.CASCADE, default=1, verbose_name=('General Category'))
    subCateDescription = models.CharField(max_length=250, default='', blank=True, null=True, verbose_name=('Sub Category Description'))
    subCateImage = models.ImageField(upload_to='subCategory/', blank=True, validators=[FileExtensionValidator(['png','jpg','jpeg'])], verbose_name=('Sub Category Image'))

    class Meta:
        verbose_name = ("Sub Category")
        verbose_name_plural = ("Sub Categories")

    def __str__(self):
        return self.subCateName

