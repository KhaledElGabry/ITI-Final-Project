from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator

class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
    ]

    first_name = models.CharField(max_length=10, blank=True, validators=[MinLengthValidator(limit_value=3), MaxLengthValidator(limit_value=30)])
    last_name = models.CharField(max_length=10, blank=True, validators=[MinLengthValidator(limit_value=3), MaxLengthValidator(limit_value=30)])
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None
    # username = models.CharField(max_length=25)
    USERNAME_FIELD = 'email'
    phone = models.CharField(max_length=11)
    usertype = models.CharField(choices=USER_TYPE_CHOICES)
    address = models.CharField(max_length=100)
    shopname = models.CharField(max_length=100, blank=True, null=True)
    ssn = models.CharField(max_length=14, blank=True)
    # rate = models.IntegerField(blank=True , default=0)
    REQUIRED_FIELDS = ['first_name', 'last_name']


    @classmethod
    def usersList(self):
        return self.objects.all()
    
   
    
    

    
