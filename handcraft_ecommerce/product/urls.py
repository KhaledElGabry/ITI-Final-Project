from django.urls import path
from . import views
# from . import api 



urlpatterns = [

     # product API's
     path('product/', views.productListApi, name='productListApi'),
     path('product/<int:id>', views.productDetailsApi, name='productDetailsApi'),


     # category API's
     path('category/', views.categoryListApi, name='categoryListApi'),
     path('category/<int:id>', views.categoryDetailsApi, name='categoryDetailsApi'),

     # sub category API's
     path('subcategory/', views.subCategoryListApi, name='subCategoryListApi'),
     path('subcategory/<int:id>', views.subCategoryDetailsApi, name='subCategoryDetailsApi'),


     

]