
from django.urls import path
from .views import  * 


urlpatterns = [
    path('new/',new_order, name='new_order'),
    path('customer/',get_customer_orders, name='get_orders'),
    path('vendor/',get_vendor_orders, name='get_orders'),
    path('<int:pk>/',get_order, name='get_order'),
    path('process_order/<int:pk>/', process_order, name='process_order'),
    path('delete_order/<int:pk>/', delete_order, name='delete_order'),
    path('create-checkout-session/<pk>/',CreateCheckOutSession.as_view(), name='checkout_session'),
    path('handle-payment-success/', handle_payment_success, name='handle_payment_success')
]