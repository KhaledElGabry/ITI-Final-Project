from django.urls import path
from . import views
# from . import api 



urlpatterns = [

     # product API's
     path('product/', views.productListApi, name='productListApi'),
     path('product/<int:id>', views.productDetailsApi, name='productDetailsApi'),

]