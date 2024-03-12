from django.urls import path
from .views import *

urlpatterns = [
        path('add/', addToCart),
        path('delete/<int:cart_id>', deleteCart),
        path('remove/<int:cart_id>', reduceCartItemQuantity),
        path('addmore/<int:cart_id>', increaseCartItemQuantity),
        path('list/', listCartItems),
        
        path('delete-all/', deleteAllCartProducts),
]