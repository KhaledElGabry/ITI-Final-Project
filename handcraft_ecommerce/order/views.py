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
    user = request.user
    # Retrieve the cart associated with the current user
    cart = get_object_or_404(Cart, user=request.user)

    # Check if the cart is empty
    if cart.cartitems.count() == 0:
        return Response({'error': "Cart is empty. Cannot create an order."}, status=status.HTTP_400_BAD_REQUEST)

    # Extract address and phone number from the request data
    address = request.data.get("address")
    phone_number = request.data.get("phone_number")
     # Delete all unpaid orders for the user
    Order.objects.filter(payment_status=PaymentStatus.UNPAID, is_paid=False, user=user).delete()

    # Create the order
    order = Order.objects.create(
        address=address,
        phone_number=phone_number,
        payment_status='Unpaid',
        payment_mode='COD',
        is_paid=False,
        user_id=user.id,
        status=Order.PENDING_STATE
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


from django.db import transaction
from .models import PaymentStatus
from cart.models import CartItem

@api_view(['POST'])  
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def handle_payment_success(request):
    if request.method == 'POST':
        user = request.user
        try:
            with transaction.atomic():
               
                # Retrieve the first remaining unpaid order for the user
                order = Order.objects.filter(payment_status=PaymentStatus.UNPAID, is_paid=False, user=user).first()

                if order:
                    # Update order status to Paid and mark it as paid
                    order.payment_status = PaymentStatus.PAID
                    order.is_paid = True
                    order.status=Order.SHIPPED_STATE
                    order.save()

                    # Clear the items from the user's cart
                    CartItem.objects.filter(cart__user=user).delete()
                    for order_item in order.orderitems.all():
                        product = order_item.product
                        if product.prodStock >= order_item.quantity:
                            product.prodStock -= order_item.quantity
                            product.save()
                        else:
                            print(f"Stock Out! Not enough prodStock for {product.prodName}.")

                    return Response({"message": "Payment success. Order marked as paid and cart cleared successfully."}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "No unpaid order found for the user."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"detail": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# customer 

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_customer_orders(request):
    user = request.user  # Get the authenticated user

    # Filter orders for the authenticated user
    orders = Order.objects.filter(user=user)

    order_data = []
    for order in orders:
        order_items = order.orderitems.all()
        items_data = []
        for item in order_items:
            items_data.append({
                'product_name': item.product.prodName,
                'quantity': item.quantity,
                'product_image_thumbnail': item.product.prodImageThumbnail.url if item.product.prodImageThumbnail else None,
                'item_id':item.product.id
            })
        order_data.append({
            'order_id': order.id,
            'address': order.address,
            'phone_number': order.phone_number,
            'payment_status': order.payment_status,
            'payment_mode': order.payment_mode,
            'is_paid': order.is_paid,
            'user': order.user.id if order.user else None,
            'status': order.status,
            'order_items': items_data,  # Include the list of order items
            'total_price': order.total_price
        })

    return Response({'orders': order_data})




# vendor 
from account.models import User
from account.serializers import *
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_vendor_orders(request):
    vendor = request.user  # Assuming the vendor is associated with the authenticated user

    # Filter products created by the vendor
    products = Product.objects.filter(prodVendor=vendor)

    # Get orders associated with these products
    orders = Order.objects.filter(orderitems__product__in=products).distinct()

    order_data = []
    for order in orders:
        # Get order items associated with the current order
        order_items = order.orderitems.filter(product__prodVendor=vendor)

        # Initialize list to hold product details for each order item
        product_details = []

        # Initialize total price for the order
        total_price = 0

        # Fetch product details for each order item
        for order_item in order_items:
            product_details.append({
                'product_name': order_item.product.prodName,
                'product_price': order_item.product.prodPrice,
                'product_description': order_item.product.prodDescription,
                'product_image_thumbnail': order_item.product.prodImageThumbnail.url if order_item.product.prodImageThumbnail else None,
                'stock': order_item.product.prodStock,
                'quantity': order_item.quantity,
            })

            # Add the price of each product to the total price
            total_price += order_item.product.prodPrice
        
        # Serialize user object
        user_data = UserSerializer(order.user).data

        # Construct order data
        order_data.append({
            'order_id': order.id,
            'address': order.address,
            'phone_number': order.phone_number,
            'payment_status': order.payment_status,
            'payment_mode': order.payment_mode,
            'is_paid': order.is_paid,
            'user': user_data,
            'status': order.status,
            'total_price': total_price,  # Include total price for all products in the order
            'products': product_details  # Include product details for each order item
        })

    return Response({'orders': order_data})