from django.contrib import admin
from .models import Product, Category, SubCategory , Rating

# admin.site.register(ProductImage)




class ProductAdmin(admin.ModelAdmin):
    list_display=['prodName','prodVendor','prodPrice']
    list_editable=['prodPrice']
    search_fields=['prodName']
    list_filter=['prodName']

admin.site.register(Product,ProductAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display=['cateName','cateDescription']
    list_editable=['cateDescription']
    search_fields=['cateName']
admin.site.register(Category,CategoryAdmin)

class SubCategoryAdmin(admin.ModelAdmin):
    list_display=['subCateName','subCateParent','subCateDescription']
    list_editable=['subCateParent','subCateDescription']
    search_fields=['subCateName']
admin.site.register(SubCategory,SubCategoryAdmin)

class RatingAdmin(admin.ModelAdmin):
    list_display=['rateProduct','rateCustomer','rateRating']
    search_fields=['rateProduct']
admin.site.register(Rating,RatingAdmin)

