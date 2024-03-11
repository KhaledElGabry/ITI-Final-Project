from django.urls import path , include
from . import views 
from rest_framework import routers

# from .views import Favorite, product_rat
# from .views import  product_rat

router=routers.DefaultRouter()
router.register('search',
                views.AllProductSearch,
                basename='search-product')


router.register('rating',
                views.RatingSearch,
                basename='Rating')

router.register('favorite',
                views.Favorite,
                basename='Favorite')

urlpatterns = [



     # product list & details API's (FunctionBasedView)
     path('', views.productListApi, name='productListApi'),
     path('details/<int:id>/', views.productDetailsApi, name='productDetailsApi'),

     # vendor API's (FunctionBasedView)
     path('vendor/', views.productVendorApi, name='productVendorApi'), 
     path('create/', views.productCreateVendorApi, name='productCreateVendorApi'),
     path('<int:id>/', views.productUpdateDeleteApi, name='productUpdateDeleteApi'),




     # vendor API's (ClassBasedView)

     path('v2/create/', views.ProductCreate.as_view(), name='product-create'),
     path('v2/update/<int:pk>', views.ProductUpdate.as_view(), name='product-update'),
     path('v2/delete/<int:pk>', views.ProductDelete.as_view(), name='product-delete'),




     # category API's (FunctionBasedView)
     path('category/', views.categoryListApi, name='categoryListApi'),
     path('category/<int:id>/', views.categoryDetailsApi, name='categoryDetailsApi'),

     # sub category API's (FunctionBasedView)
     path('subcategory/', views.subCategoryListApi, name='subCategoryListApi'),
     path('subcategory/<int:id>/', views.subCategoryDetailsApi, name='subCategoryDetailsApi'),

     # favorite prod
     # path('product_r/<int:id>/',views.product_rat),
     
#      path('api/favorite/', Favorite.as_view({'get': 'list'}), name='favorite-list'),
#     path('api/product/<int:id>/rating/', product_rat, name='product-rating-api'),

     # all product url for search bar
     path('',include(router.urls)),

]
app_name='products'
