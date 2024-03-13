from django.db import models
from django.conf import settings
from product.models import Product


class Cart(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, blank=True)
  item = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
  quantity = models.IntegerField(default=1)

  def __str__(self):
        return f"{self.id} of {self.item.name}"

  def get_total_item_price(self):
      return self.quantity * self.item.prodPrice