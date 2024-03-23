from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import views
from rest_framework.response import Response
from rest_framework.decorators import api_view
from cart.models import *
from .serializers import CartItemSerializer
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes, authentication_classes
from django.core.exceptions import ObjectDoesNotExist
from account.models import CustomToken
from rest_framework.exceptions import AuthenticationFailed
import stripe
from order.models import Order, OrderItem
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.http import JsonResponse
from django.contrib.auth.models import User  # Import the User model
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def addToCart(request):
    if request.user.usertype == "vendor":
        raise AuthenticationFailed({"message": 'Only customers can access.'})
        
    try:
        token = CustomToken.objects.get(user=request.user)
        if token.expires and token.is_expired():
            raise AuthenticationFailed({"data": "expired_token.", "message": 'Please login again.'})
    except CustomToken.DoesNotExist:
        raise AuthenticationFailed({"data": "token_missing.", "message": 'Please provide a valid token.'})
    
    item_id = request.data.get("item")
    quantity = request.data.get("quantity")

    try:
        item = Product.objects.get(id=item_id)
    except ObjectDoesNotExist:
        return Response({'msg': 'Product does not exist'}, status=status.HTTP_404_NOT_FOUND)

    # Ensure that the cart is associated with the current user
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)

    if int(quantity) > item.prodStock:
        return Response({'msg': 'Requested quantity exceeds available stock'}, status=status.HTTP_400_BAD_REQUEST)
    cart_items = cart.cartitems.all()
    cart_item.quantity += int(quantity)
    cart_item.save()
    total_items_count = sum(cart_item.quantity for cart_item in cart_items)
    total_item_price = cart_item.get_total_item_price()
    return Response({'msg': 'added', 'total_item_price': total_item_price, 'quantity': cart_item.quantity,'total_items_count':total_items_count}, status=status.HTTP_201_CREATED)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def listCartItems(request):
    try:
        token = CustomToken.objects.get(user=request.user)
        if token.expires and token.is_expired():
            raise AuthenticationFailed({"data": "expired_token.", "message": 'Please login again.'})

        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.cartitems.all()
        serializer = CartItemSerializer(cart_items, many=True)  # Use CartItemSerializer instead of CartSerializer

        if not cart_items:
            return Response({'msg': 'Cart is empty'}, status=status.HTTP_200_OK)

        total_items_price = sum(cart_item.get_total_item_price() for cart_item in cart_items)+10
        total_items_count = sum(cart_item.quantity for cart_item in cart_items)

        response_data = {
            'cart_items': serializer.data,
            'total_items_price': total_items_price,
            'total_items_count': total_items_count,
        }

        return Response(response_data)
    except CustomToken.DoesNotExist:
        raise AuthenticationFailed({"data": "token_missing.", "message": 'Please provide a valid token.'})
    
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def deleteCart(request, cart_item_id):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id, cart__user=request.user)
        cart_item.delete()
        return Response({'msg': 'deleted'}, status=status.HTTP_200_OK)
    except Cart.DoesNotExist:
        return Response({'msg': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def reduceCartItemQuantity(request, cart_item_id):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id, cart__user=request.user)

        if request.method == 'PUT':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
                total_item_price = cart_item.get_total_item_price()
                return Response({'msg': 'Quantity reduced successfully', 'total_item_price': total_item_price}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'Quantity cannot be reduced further'}, status=status.HTTP_400_BAD_REQUEST)
    except Cart.DoesNotExist:
        return Response({'msg': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)

    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def increaseCartItemQuantity(request, cart_item_id):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id, cart__user=request.user)

        if request.method == 'PUT':
            if cart_item.item.prodStock > cart_item.quantity:  # Check if increasing quantity exceeds prodStock limit
                cart_item.quantity += 1
                cart_item.save()

                # Recalculate total item price
                total_item_price = cart_item.get_total_item_price()

                return Response({'msg': 'Quantity increased successfully', 'total_item_price': total_item_price}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'Quantity cannot be increased further, exceeds prodStock limit'}, status=status.HTTP_400_BAD_REQUEST)
    except CartItem.DoesNotExist:
        return Response({'msg': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def deleteAllCartProducts(request):
    try:
        # Get all cart items for the authenticated user
        cart_items = Cart.objects.filter(user=request.user)
        
        # Delete all cart items
        cart_items.delete()
        
        return Response({'msg': 'All cart products deleted'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'msg': 'Failed to delete cart products', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)













# #payment
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









