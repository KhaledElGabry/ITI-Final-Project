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
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response({'orders': serializer.data})

@api_view(['GET'])
def get_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    serializer = OrderSerializer(order)
    return Response({'order': serializer.data})

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def process_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    serializer = OrderSerializer(order, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'order': serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    order.delete()
    return Response({'details': "order is deleted"})
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
    cart.cartitems.all().delete()

    # Serialize the order
    serializer = OrderSerializer(order)

    return Response(serializer.data, status=status.HTTP_201_CREATED)
