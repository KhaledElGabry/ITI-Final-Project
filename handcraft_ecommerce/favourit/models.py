from django.db import models
from account.models import User
from product.models import Product

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Favorite"
        verbose_name_plural = "Favorites"

    def __str__(self):
        return f"{self.user.username}'s favorite: {self.product.prodName}"
