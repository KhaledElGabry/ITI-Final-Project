from django.urls import path , include
from . import views

urlpatterns = [

    # log-in // log-out 
    path('admin_login/',views.admin_login,name='login'),
    path('admin_logout/',views.admin_logout,name='logout'),

    # User
    path('specific_user/<int:id>/',views.specific_user,name='specific_user'),
    path('userDetails/',views.userDetails,name='userDetails'),
    path('addUser/',views.useradd,name='addUser'),
    path('delUser/<int:id>/',views.delete,name='delUser'),
    path('updateUser/<int:id>/',views.update,name='updateUser'),

    # Product
    path('specific_product/<int:id>/',views.specific_product,name='specific_product'),
    path('productDetails/',views.productDetails,name='productDetails'),
    path('productadd/',views.productadd,name='productadd'),
    path('delproduct/<int:id>/',views.delproduct,name='delproduct'),
    path('updateproduct/<int:id>/',views.updateproduct,name='delproduct'),

    # Category
    path('specific_category/<int:id>/',views.specific_category,name='specific_category'),
    path('categoryDetails/',views.categoryDetails,name='categoryDetails'),
    path('categoryadd/',views.categoryadd,name='categoryadd'),
    path('delcategory/<int:id>/',views.delcategory,name='delcategory'),
    path('updatecategory/<int:id>/',views.updatecategory,name='updatecategory'),

    # sub Category
    path('spcific_subcategory/<int:id>/',views.spcific_subcategory,name='spcific_subcategory'),
    path('subcategoryDetails/',views.subcategoryDetails,name='subcategoryDetails'),
    path('addsub_category/',views.addsub_category,name='addsub_category'),
    path('delsub_category/<int:id>/',views.delsub_category,name='delsub_category'),
    path('updatesub_CateName/<int:id>/',views.updatesub_CateName,name='updatesub_CateName'),
    
    path('count-prod-user/', views.countAllProductsAndUsers, name='products_and_users'),
]