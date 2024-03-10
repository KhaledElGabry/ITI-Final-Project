from django.urls import path , include
from . import views 
from rest_framework import routers


router=routers.DefaultRouter()
router.register('search',
                views.productserializer,
                basename='search-product')


router.register('rating',
                views.Ratingserlizer,
                basename='Rating')

router.register('favorite',
                views.Favorite,
                basename='Favorite')

urlpatterns = [

     # product API's
     path('product/', views.productListApi, name='productListApi'),
     path('product/<int:id>', views.productDetailsApi, name='productDetailsApi'),

     # vendor API's
     path('product/vendor/<int:id>', views.productVendorApi, name='productVendorApi'), 
     path('product/create', views.productCreateVendorApi, name='productCreateVendorApi'),
     path('product/update_delete/<int:id>', views.productUpdateDeleteApi, name='productUpdateDeleteApi'),



     # category API's
     path('category/', views.categoryListApi, name='categoryListApi'),
     path('category/<int:id>', views.categoryDetailsApi, name='categoryDetailsApi'),

     # sub category API's
     path('subcategory/', views.subCategoryListApi, name='subCategoryListApi'),
     path('subcategory/<int:id>', views.subCategoryDetailsApi, name='subCategoryDetailsApi'),

     # all product url for search bar
     path('',include(router.urls)),
]
app_name='products'
