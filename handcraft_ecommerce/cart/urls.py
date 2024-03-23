from django.urls import path
from .views import *

urlpatterns = [
        path('add/', addToCart),
        path('delete/<int:cart_item_id>', deleteCart),
        path('remove/<int:cart_item_id>', reduceCartItemQuantity),
        path('addmore/<int:cart_item_id>', increaseCartItemQuantity),
        path('list/', listCartItems),
        
        path('delete-all/', deleteAllCartProducts),
        path('create-checkout-session/<pk>/',CreateCheckOutSession.as_view(), name='checkout_session'),
        
        path('handle/', handle_payment_success, name='handle_payment_success'),
]