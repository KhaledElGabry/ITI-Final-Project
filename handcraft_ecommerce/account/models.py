from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    usertype = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    address = models.CharField(max_length=100)
    shopname = models.CharField(max_length=100, blank=True, null=True)
    ssn = models.CharField(blank=True)
    rate = models.IntegerField(blank=True , default=0)