from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import OrderSerializer
from .models import Order, OrderItem
from product.models import Product
from cart.models import Cart
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
from django.conf import settings
import stripe
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.http import JsonResponse

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_orders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response({'orders': serializer.data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    serializer = OrderSerializer(order)
    return Response({'order': serializer.data})

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def process_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    serializer = OrderSerializer(order, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'order': serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def delete_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    order.delete()
    return Response({'details': "order is deleted"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def new_order(request):
    # Retrieve the cart associated with the current user
    cart = get_object_or_404(Cart, user=request.user)

    # Check if the cart is empty
    if cart.cartitems.count() == 0:
        return Response({'error': "Cart is empty. Cannot create an order."}, status=status.HTTP_400_BAD_REQUEST)

    # Extract address and phone number from the request data
    address = request.data.get("address")
    phone_number = request.data.get("phone_number")

    # Create the order
    order = Order.objects.create(
        address=address,
        phone_number=phone_number,
        payment_status='Unpaid',
        payment_mode='COD',
        is_paid=False
    )

    # Extract cart items and create order items
    order_items = []
    for cart_item in cart.cartitems.all():  # Use cart.cartitems.all() to access related CartItem objects
        order_item = OrderItem.create_from_cart(order, cart_item)
        order_items.append(order_item)

    # Associate order items with the order
    order.orderitems.set(order_items)

    # Empty the cart by deleting all cart items
   # cart.cartitems.all().delete()

    # Serialize the order
    serializer = OrderSerializer(order)

    return Response(serializer.data, status=status.HTTP_201_CREATED)


from cart.models import CartItem
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def handle_payment_success(request):
    if request.method == 'POST':
        user = request.user
        # Assuming you have a Cart model associated with the user
        try:
            cart_items = CartItem.objects.filter(cart__user=user)
            cart_items.delete()
            return Response({"message": "Cart cleared successfully."}, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({"message": "Cart is already empty."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"detail": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
# def paid(request):
#     try:
#         payload = request.data
#         # Retrieve order ID from the payload (assuming it's provided by Stripe)
#         order_id = payload['metadata']['order_id']
#         order = Order.objects.get(id=order_id)

#         # Update order status or any other necessary actions
#         order.status = 'Paid'
#         order.save()

#         return Response({'message': 'Order payment status updated to Paid.'}, status=status.HTTP_200_OK)

#     except Order.DoesNotExist:
#         return JsonResponse({'error': 'Order not found'}, status=404)

#     except Exception as e:
#         return JsonResponse({'error': 'Something went wrong while handling paid order', 'details': str(e)}, status=500)



# from .models import PaymentStatus
# @api_view(['POST'])  # Ensure it accepts POST requests
# @permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
# def handle_payment_success(request):
#     if request.method != 'POST':
#         return Response({'error': 'Method not allowed. Only POST requests are allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

#     try:
#         payload = request.data
#         # Retrieve order ID from the payload (assuming it's provided by Stripe)
#         order_id = payload['metadata']['order_id']
#         order = Order.objects.get(id=order_id)
        
#         # Mark the order as paid
#         order.payment_status = PaymentStatus.PAID
#         order.is_paid = True
#         order.save()

#         # Clear the cart associated with the user
#         cart = get_object_or_404(Cart, user=request.user)
#         # cart.cartitems.all().delete()

#         # Retrieve order items
#         order_items = OrderItem.objects.filter(order=order)

#         # Prepare response data
#         paid_products_info = []
#         for order_item in order_items:
#             product = order_item.product
#             quantity = order_item.quantity
#             remaining_stock = product.prodStock
#             customer_details = {
#                 'name': order.address,  # Assuming the address contains the customer's name
#                 'phone_number': order.phone_number,
#                 # Add more customer details if needed
#             }
#             paid_products_info.append({
#                 'product_name': product.prodName,
#                 'quantity': quantity,
#                 'remaining_stock': remaining_stock,
#                 'customer_details': customer_details
#             })

#         # Update order status or any other necessary actions

#         return Response({'message': 'Payment successful and cart cleared.', 'paid_products_info': paid_products_info}, status=status.HTTP_200_OK)
    

#     except Order.DoesNotExist:
#         return JsonResponse({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

#     except Exception as e:
#         return JsonResponse({'error': 'Something went wrong while handling payment success', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def paid_products_list(request):
#     try:
#         # Retrieve paid orders
#         paid_orders = Order.objects.filter(payment_status='Paid')

#         # Prepare response data
#         paid_products_info = []
#         for order in paid_orders:
#             order_items = OrderItem.objects.filter(order=order)
#             for order_item in order_items:
#                 product = order_item.product
#                 quantity = order_item.quantity
#                 remaining_stock = product.prodStock
#                 customer_details = {
#                     'name': order.address,  # Assuming the address contains the customer's name
#                     'phone_number': order.phone_number,
#                     # Add more customer details if needed
#                 }
#                 paid_products_info.append({
#                     'product_name': product.prodName,
#                     'quantity': quantity,
#                     'remaining_stock': remaining_stock,
#                     'customer_details': customer_details
#                 })

#         return Response({'paid_products_info': paid_products_info}, status=status.HTTP_200_OK)

#     except Exception as e:
#         return Response({'error': 'Something went wrong while retrieving paid products', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
