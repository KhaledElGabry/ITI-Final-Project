from tabnanny import verbose
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator


class Product(models.Model):
     prodName = models.CharField(max_length=100, on_delete=models.CASCADE, verbose_name=('Product Name'))
     prodPrice = models.DecimalField(default=0, decimal_places=2, max_digits=5, verbose_name=('Product Price'))
     prodQuantity = models.IntegerField(default=1, verbose_name=('Product Quantity'))
     prodDescription = models.TextField(max_length=450, default='', blank=False, null=False, verbose_name=('Product Description'))
     prodCategory = models.ForeignKey('Category', on_delete=models.CASCADE, default=1, verbose_name=('Category Name'))
     prodSubCategory = models.ForeignKey('SubCategory', on_delete=models.CASCADE, default=1, verbose_name=('Sub Category Name'),)
     prodOnSale = models.BooleanField(default=False, verbose_name=('On Sale'))
     prodRating = models.FloatField(default=0.0, validators=[MinValueValidator(0.0, "Rating must be at least 0.0"), MaxValueValidator(5.0, "Rating cannot exceed 5.0")], verbose_name=('Rate'))
     # prodSlug = models.SlugField(blank=True, null=True)
     # prodImageCover = models.ImageField(upload_to='product/', default='static/covers/no-product.png', validators=[FileExtensionValidator(['png','jpg','jpeg'])], verbose_name=('Product Image Cover'))
     prodImages = models.ManyToManyField('ProductImage', blank=False)

     class Meta:
          verbose_name= ('Product')
          verbose_name_plural= ('Products')

     # def save(self, *args, **kwargs):
     #      if not self.prodSlug:
     #           self.prodSlug = slugify(self.prodName)
     #      super(Product, self).save(*args, **kwargs)
          
     def __str__(self):
          return self.prodName
     

class ProductImage(models.Model):
     # prodImageProduct = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=('Product'))
     prodImage = models.ImageField(upload_to='product/', validators=[FileExtensionValidator(['png','jpg','jpeg'])], verbose_name=('Product Image'))

     class Meta:
          verbose_name = ("Product Image")
          verbose_name_plural = ("Product Images")

     def __str__(self):
          return str(self.prodImage)




class Category(models.Model):
     cateName = models.CharField(max_length=50, verbose_name=('Category Name'))
     # cateParent = models.ForeignKey('self', limit_choices_to={'cateParent__isnull':True}, on_delete=models.CASCADE, blank=True, null=True, verbose_name=('General Category'))
     cateDescription = models.CharField(max_length=250, default='', blank=False, null=False, verbose_name=('Category Description'))
     cateImage = models.ImageField(upload_to='category/', validators=[FileExtensionValidator(['png','jpg','jpeg'])], verbose_name=('Category Image'))

     class Meta:
          verbose_name = ("Category")
          verbose_name_plural = ("Categories")

     def __str__(self):
          return self.cateName


class SubCategory(models.Model): 
     subCateName = models.CharField(max_length=50, verbose_name=('Sub Category Name'))
     subCateParent = models.ForeignKey(Category, on_delete=models.CASCADE, default=1, verbose_name=('General Category'))
     subCateDescription = models.CharField(max_length=250, default='', blank=False, null=False, verbose_name=('Sub Category Description'))
     subCateImage = models.ImageField(upload_to='subCategory/', validators=[FileExtensionValidator(['png','jpg','jpeg'])], verbose_name=('Sub Category Image'))

     class Meta:
          verbose_name = ("Sub Category")
          verbose_name_plural = ("Sub Categories")

     def __str__(self):
          return self.subCateName