from django.db import models
from product.models import Product
from cart.models import Cart
from django.conf import settings
from account.models import User
class PaymentStatus(models.TextChoices):
    PAID = 'Paid'
    UNPAID = 'Unpaid'

class PaymentMode(models.TextChoices):
    COD = 'COD'
    CARD = 'CARD'

class Order(models.Model):
    address = models.CharField(max_length=100, default="", blank=False)
    phone_number = models.CharField(max_length=100, default="", blank=False)
    payment_status = models.CharField(max_length=30, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)
    payment_mode = models.CharField(max_length=30, choices=PaymentMode.choices, default=PaymentMode.COD)
    is_paid = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return str(self.id)

    @property
    def total_price(self):
        # Calculate total price of all items in the order
        return sum(item.total_item_price for item in self.orderitems.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="orderitems", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product.prodName

    @property
    def total_item_price(self):
        # Calculate total price of this item in the order
        return self.quantity * self.product.prodPrice

    @classmethod
    def create_from_cart(cls, order, cart_item):
        # Create and save an OrderItem instance from a Cart item
        order_item = cls(
            order=order,
            product=cart_item.item,
            quantity=cart_item.quantity
        )
        order_item.save()  # Save the OrderItem instance
        return order_item