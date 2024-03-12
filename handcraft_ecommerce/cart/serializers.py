from rest_framework import serializers
from cart.models import *


class CartSerlizer(serializers.ModelSerializer):
    item_image = serializers.ImageField(source='item.image', read_only=True)
    item_name = serializers.CharField(source='item.name', read_only=True)
    item_price = serializers.DecimalField(source='item.price', read_only=True, max_digits=10, decimal_places=2)
    subtotal_price = serializers.SerializerMethodField()
    
    def get_subtotal_price(self, obj):
        return obj.quantity * obj.item.prodPrice
    class Meta:
        model = Cart
        fields = '__all__'



    def create(self, validated_data):
        # ** means 3aml el validate data k dict
        return Cart.objects.create(**validated_data)