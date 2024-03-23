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


#payment
stripe.api_key=settings.STRIPE_SECRET_KEY
success_url = settings.SITE_URL 
API_URL="http/locahost:8000"
class CreateCheckOutSession(APIView):
    def post(self, request, *args, **kwargs):
        order_id = kwargs.get("pk")  # Get the order ID from URL parameters
        try:
            order = Order.objects.get(id=order_id)  # Retrieve the order from the database

            # Create a Stripe Checkout session
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': int(order.total_price) * 100,
                            'product_data': {
                                'name': str(order.pk),
                                # 'images': [f"{API_URL}/{orderitem_id.product_image}"]
                            }
                        },
                        'quantity': 1,
                    },
                ],
                metadata={"order_id": order.id},
                mode='payment',
                success_url=settings.SITE_URL + 'handle-payment-success/',  # Updated success_url
                cancel_url=settings.SITE_URL + '?canceled=true',
                


       
            )

            # Redirect the user to the Stripe Checkout URL
            return redirect(checkout_session.url)
        
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
        
        except Exception as e:
            return JsonResponse({'error': 'Something went wrong while creating stripe session', 'details': str(e)}, status=500)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
# def handle_payment_success(request):
#     try:
#         payload = request.data
#         print(payload)
#         # Retrieve order ID from the payload (assuming it's provided by Stripe)
#         order_id = payload['metadata']['order_id']
#         order = Order.objects.get(id=order_id)
        
#         order.is_paid = True
#         order.save() 

#         # Clear the cart associated with the user
#         cart = get_object_or_404(Cart, user=request.user)
#         # cart.cartitems.all().delete()
        
#         return Response({'message': 'Payment successful and cart cleared.'}, status=status.HTTP_200_OK)

#     except Order.DoesNotExist:
#         return JsonResponse({'error': 'Order not found'}, status=404)

#     except Exception as e:
#         return JsonResponse({'error': 'Something went wrong while handling payment success', 'details': str(e)}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def handle_payment_success(request):
    try:
        payload = request.data
        print(payload)
        # Retrieve order ID from the payload
        order_id = payload['metadata']['order_id']
        order = Order.objects.get(id=order_id)
        order.is_paid = True
        order.save()
        
        for order_item in order.orderitems.all():
            product = order_item.product
            if product.stock >= order_item.quantity:
                product.stock -= order_item.quantity
                product.save()
            else:
                print(f"Stock Out! Not enough stock for {product.prodName}.")
                
        cart = get_object_or_404(Cart, user=request.user)
        cart.cartitems.all().delete()
        return Response({'message': 'Payment successful and cart cleared. Stock updated.', 'status': status.HTTP_200_OK})
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)

    except Exception as e:
        return JsonResponse({'error': 'Something went wrong while handling payment success', 'details': str(e)}, status=500)
