from django.urls import path , include
from . import views 
from rest_framework import routers

# from .views import Favorite, product_rat
# from .views import  product_rat

router=routers.DefaultRouter()
router.register('search',
                views.AllProductSearch,
                basename='search-product')

urlpatterns = [



     # Product list & details API's 
     path('', views.productListApi, name='productListApi'), 
     path('details/<int:id>/', views.productDetailsApi, name='productDetailsApi'),
     path('vendor/<int:id>/', views.vendorProductDetailsApi, name='vendorProductDetailsApi'),
     path('lastProducts/', views.lastProducts, name='productDetailsApi'),




     # Vendor CRUD Operations API's 
     path('vendor/', views.productVendorApi, name='productVendorApi'), 
     path('create/', views.productCreateVendorApi, name='productCreateVendorApi'),
     path('<int:id>/', views.productUpdateDeleteApi, name='productUpdateDeleteApi'),



     # category API's (FunctionBasedView)
     path('category/', views.categoryListApi, name='categoryListApi'),
     path('category/<int:id>/', views.categoryDetailsApi, name='categoryDetailsApi'),

     # sub category API's (FunctionBasedView)
     path('subcategory/', views.subCategoryListApi, name='subCategoryListApi'),
     path('subcategory/<int:id>/', views.subCategoryDetailsApi, name='subCategoryDetailsApi'),

 
     # favorite prod
    path('add_to_Favorite/<int:id>/',views.add_to_Favorite, name='add_to_Favorite'),
    path('remove_from_Favorite/<int:id>/',views.remove_from_Favorite, name='remove_from_Favorite'),
    path('user_favorite/',views.user_favorite, name='user_favorite'),

     #  rating 
     path('product_r/<int:id>/',views.product_rat),
     path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),

     # chatbot
     # path('getResponse/',views.get_response,name='getResponse/'),

     # all product url for search bar
     path('',include(router.urls)),

]
app_name='products'
