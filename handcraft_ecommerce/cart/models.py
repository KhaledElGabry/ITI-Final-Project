from django.db import models
from django.conf import settings
from product.models import Product
from product.serializers import *
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems')
    item = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} of {self.item.prodName}"

    def get_total_item_price(self):
        # Calculate total item price based on the discounted price of the product
        if self.item.prodOnSale:
            discounted_price = ProductSerializer().get_discounted_price(self.item)
            return self.quantity * discounted_price
        else:
            return self.quantity * self.item.prodPrice