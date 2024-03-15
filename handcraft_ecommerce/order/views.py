from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import OrderSerializer
from .models import Order, OrderItem
from product.models import Product
from cart.models import Cart , CartItem
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
    # 

    # Serialize the order
    serializer = OrderSerializer(order)

    return Response(serializer.data, status=status.HTTP_201_CREATED)


#payment
stripe.api_key=settings.STRIPE_SECRET_KEY
success_url = settings.SITE_URL + 'thannk-you/'
API_URL="http/locahost:8000"
class CreateCheckOutSession(APIView):
      def post(self, request, *args, **kwargs):
        order_id = kwargs.get("pk")  
        try:
            order = Order.objects.get(id=order_id)  

            cart = get_object_or_404(Cart, user=request.user)
            order_items = OrderItem.objects.filter(order=order)

            
            cart_items = CartItem.objects.filter(item__in=[item.product for item in order_items])

        
            total_price = sum(item.get_total_item_price() for item in cart_items)

            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': int(total_price * 100), 
                            'product_data': {
                                'name': str(order.address),
                            }
                        },
                        'quantity': 1,
                    },
                ],
                metadata={"order_id": order.id},
                mode='payment',
                success_url=settings.SITE_URL + 'thank-you/',  
                cancel_url=settings.SITE_URL + '?canceled=true',
            )

            cart.cartitems.all().delete()
            return redirect(checkout_session.url)

        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)

        except Exception as e:
            return JsonResponse({'error': 'Something went wrong while creating stripe session', 'details': str(e)}, status=500)