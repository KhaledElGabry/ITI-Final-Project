from rest_framework import serializers
from cart.models import CartItem
from product.serializers import ProductSerializer

class CartItemSerializer(serializers.ModelSerializer):
    item_image = serializers.ImageField(source='item.prodImageThumbnail', read_only=True)
    item_name = serializers.CharField(source='item.prodName', read_only=True)
    item_description = serializers.CharField(source='item.prodDescription', read_only=True)
    subtotal_price = serializers.SerializerMethodField()
    item_price = serializers.SerializerMethodField()

    def get_subtotal_price(self, obj):
        return obj.quantity * obj.item.prodPrice

    def get_item_price(self, obj):
        product_serializer = ProductSerializer(obj.item)
        return product_serializer.data['discounted_price']

    class Meta:
        model = CartItem
        fields = ['id', 'item_image', 'item_name', 'item_description', 'quantity', 'subtotal_price', 'item_price', 'item_id']
