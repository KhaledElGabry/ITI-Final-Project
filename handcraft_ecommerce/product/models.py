from django.db import models
from django.core.validators import FileExtensionValidator
from account.models import User

class Product(models.Model):
    prodVendor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    prodName = models.CharField(max_length=100, verbose_name=('Product Title'))
    prodPrice = models.DecimalField(default=0, decimal_places=2, max_digits=5, verbose_name=('Product Price'))
    prodDescription = models.TextField(max_length=450, default='', blank=True, null=True, verbose_name=('Product Description'))
    prodSubCategory = models.ForeignKey('SubCategory', on_delete=models.CASCADE, default=1, verbose_name=('Sub Category Name'),)
    prodOnSale = models.BooleanField(default=False, verbose_name=('On Sale'))
    prodImageThumbnail = models.ImageField(upload_to='product/', default='thumbnails/no-product.png', validators=[FileExtensionValidator(['png','jpg','jpeg'])], verbose_name=('Image Thumbnail'))

    class Meta:
        verbose_name = ('Product')
        verbose_name_plural = ('Products')

    def __str__(self):
        return self.prodName

class ProductImage(models.Model):
    prodImageProduct = models.ForeignKey(Product, on_delete=models.CASCADE, default=None, verbose_name=('Product'))
    prodImage = models.ImageField(upload_to='product/', validators=[FileExtensionValidator(['png','jpg','jpeg'])], verbose_name=('Product Images'))

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
