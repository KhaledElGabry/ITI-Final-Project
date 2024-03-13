from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import views
from rest_framework.response import Response
from rest_framework.decorators import api_view
from cart.models import *
from .serializers import CartSerlizer
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes, authentication_classes
from django.core.exceptions import ObjectDoesNotExist
from account.models import CustomToken
from rest_framework.exceptions import AuthenticationFailed
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def addToCart(request):
    if request.user.usertype == "vendor":
        raise AuthenticationFailed({"message": 'only customer can access.'})
        
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
        item_prodStock = item.prodStock
    except ObjectDoesNotExist:
        return Response({'msg': 'Product does not exist'}, status=status.HTTP_404_NOT_FOUND)

    data = {'item': item_id, 'quantity': quantity}

    if Cart.objects.filter(item=item, user=request.user).exists():
        existing_cart_item = Cart.objects.get(item=item, user=request.user)
        new_quantity = existing_cart_item.quantity + int(quantity)
        if new_quantity <= int(item_prodStock):
            existing_cart_item.quantity = new_quantity
            existing_cart_item.save()
            total_item_price = existing_cart_item.get_total_item_price()
            return Response({'msg': 'Quantity updated in cart', 'total_item_price': total_item_price, 'quantity': new_quantity}, status=status.HTTP_200_OK)
        else:
            existing_cart_item.quantity = int(item_prodStock)
            existing_cart_item.save()
            return Response({'msg': 'Quantity exceeds prodStock limit', 'total_item_price': existing_cart_item.get_total_item_price(), 'quantity': item_prodStock}, status=status.HTTP_400_BAD_REQUEST)
    else:
        if int(item_prodStock) >= int(quantity):
            serializer = CartSerlizer(data=data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                cart = serializer.instance
                total_item_price = cart.get_total_item_price()
                return Response({'msg': 'added', 'total_item_price': total_item_price, 'quantity': quantity}, status=status.HTTP_201_CREATED)
            else:
                return Response({'msg': 'Invalid data', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            data['quantity'] = int(item_prodStock)
            serializer = CartSerlizer(data=data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                cart = serializer.instance
                total_item_price = cart.get_total_item_price()
                return Response({'msg': 'added', 'total_item_price': total_item_price, 'quantity': item_prodStock}, status=status.HTTP_201_CREATED)
            else:
                return Response({'msg': 'Invalid data', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def listCartItems(request):
    try:
        token = CustomToken.objects.get(user=request.user)
        if token.expires and token.is_expired():
            raise AuthenticationFailed({"data": "expired_token.", "message": 'Please login again.'})

        # Retrieve the user's cart items
        user_carts = Cart.objects.filter(user=request.user)
        serializer = CartSerlizer(user_carts, many=True)

        if not user_carts:
            return Response({'msg': 'Cart is empty'}, status=status.HTTP_200_OK)

        # Calculate total items price and count
        total_items_price = sum(cart_item.get_total_item_price() for cart_item in user_carts)
        total_items_count = sum(cart_item.quantity for cart_item in user_carts)

        # Prepare response data
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
def deleteCart(request, cart_id):
    try:
        obj = Cart.objects.get(id=cart_id, user=request.user)
        obj.delete()
        return Response({'msg': 'deleted'}, status=status.HTTP_200_OK)
    except Cart.DoesNotExist:
        return Response({'msg': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def reduceCartItemQuantity(request, cart_id):
    try:
        cart = Cart.objects.get(id=cart_id, user=request.user)

        if request.method == 'PUT':
            if cart.quantity > 1:
                cart.quantity -= 1
                cart.save()
                total_item_price = cart.get_total_item_price()
                return Response({'msg': 'Quantity reduced successfully','total_item_price': total_item_price}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'Quantity cannot be reduced further'}, status=status.HTTP_400_BAD_REQUEST)
    except Cart.DoesNotExist:
        return Response({'msg': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def increaseCartItemQuantity(request, cart_id):
    try:
        cart = Cart.objects.get(id=cart_id, user=request.user)

        if request.method == 'PUT':
            if cart.item.prodStock > cart.quantity:  # Check if increasing quantity exceeds prodStock limit
                cart.quantity += 1
                cart.save()

                # Recalculate total item price
                total_item_price = cart.get_total_item_price()

                return Response({'msg': 'Quantity increased successfully', 'total_item_price': total_item_price}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'Quantity cannot be increased further, exceeds prodStock limit'}, status=status.HTTP_400_BAD_REQUEST)
    except Cart.DoesNotExist:
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
