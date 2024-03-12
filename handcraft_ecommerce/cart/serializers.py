from rest_framework import serializers
from cart.models import Cart, CartItem
from account.models import User

class CartItemSerializer(serializers.ModelSerializer):
    item_image = serializers.ImageField(source='item.image', read_only=True)
    item_name = serializers.CharField(source='item.name', read_only=True)
    item_price = serializers.DecimalField(source='item.price', read_only=True, max_digits=10, decimal_places=2)
    subtotal_price = serializers.SerializerMethodField()

    def get_subtotal_price(self, obj):
        return obj.quantity * obj.item.prodPrice

    class Meta:
        model = CartItem
        fields = ['id', 'item_image', 'item_name', 'item_price', 'quantity', 'subtotal_price']

class CartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    cart_items = CartItemSerializer(many=True, read_only=True)  # Include CartItemSerializer as nested serializer
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'cart_items']  # Update fields to include 'user' and 'cart_items'
