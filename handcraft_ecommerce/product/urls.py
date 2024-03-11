from django.urls import path
from . import views 


urlpatterns = [



     # product list & details API's (FunctionBasedView)
     path('', views.productListApi, name='productListApi'),
     path('details/<int:id>/', views.productDetailsApi, name='productDetailsApi'),

     # vendor API's (FunctionBasedView)
     path('vendor/', views.productVendorApi, name='productVendorApi'), 
     path('create/', views.productCreateVendorApi, name='productCreateVendorApi'),
     path('<int:id>/', views.productUpdateDeleteApi, name='productUpdateDeleteApi'),



     # category API's (FunctionBasedView)
     path('category/', views.categoryListApi, name='categoryListApi'),
     path('category/<int:id>/', views.categoryDetailsApi, name='categoryDetailsApi'),

     # sub category API's (FunctionBasedView)
     path('subcategory/', views.subCategoryListApi, name='subCategoryListApi'),
     path('subcategory/<int:id>/', views.subCategoryDetailsApi, name='subCategoryDetailsApi'),


]