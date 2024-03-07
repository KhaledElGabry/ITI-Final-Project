from django.urls import path
from . import views 


urlpatterns = [



     # product list & details API's (FunctionBasedView)
     path('product/', views.productListApi, name='productListApi'),
     path('product/<int:id>', views.productDetailsApi, name='productDetailsApi'),

     # vendor API's (FunctionBasedView)
     path('product/vendor/<int:id>', views.productVendorApi, name='productVendorApi'), 
     path('product/create/', views.productCreateVendorApi, name='productCreateVendorApi'),
     path('product/update_delete/<int:id>', views.productUpdateDeleteApi, name='productUpdateDeleteApi'),




     # vendor API's (ClassBasedView)

     path('product/v2/create/', views.ProductCreate.as_view(), name='product-create'),
     path('product/v2/update/<int:pk>', views.ProductUpdate.as_view(), name='product-update'),
     path('product/v2/delete/<int:pk>', views.ProductDelete.as_view(), name='product-delete'),




     # category API's (FunctionBasedView)
     path('category/', views.categoryListApi, name='categoryListApi'),
     path('category/<int:id>', views.categoryDetailsApi, name='categoryDetailsApi'),

     # sub category API's (FunctionBasedView)
     path('subcategory/', views.subCategoryListApi, name='subCategoryListApi'),
     path('subcategory/<int:id>', views.subCategoryDetailsApi, name='subCategoryDetailsApi'),


]