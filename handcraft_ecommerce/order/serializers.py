from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'total_item_price']

class OrderSerializer(serializers.ModelSerializer):
    orderitems = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'address', 'phone_number', 'payment_status', 'payment_mode', 'is_paid', 'total_price', 'orderitems']
        read_only_fields = ['id', 'is_paid', 'total_price']

    def create(self, validated_data):
        orderitems_data = validated_data.pop('orderitems')
        order = Order.objects.create(**validated_data)
        for item_data in orderitems_data:
            OrderItem.objects.create(order=order, **item_data)
        return order
