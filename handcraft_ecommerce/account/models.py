from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator

class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
    ]

    first_name = models.CharField(max_length=10, validators=[MinLengthValidator(limit_value=3), MaxLengthValidator(limit_value=30)])
    last_name = models.CharField(max_length=10, validators=[MinLengthValidator(limit_value=3), MaxLengthValidator(limit_value=30)])
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None
    USERNAME_FIELD = 'email'
    phone = models.CharField(max_length=11, validators=[RegexValidator(regex='^01\d{9}$', message='Invalid phone number', code='invalid_phone')], null=True)
    usertype = models.CharField(choices=USER_TYPE_CHOICES)
    address = models.CharField(max_length=100, null=True)
    shopname = models.CharField(max_length=100, null=True)
    ssn = models.CharField(max_length=14, validators=[RegexValidator(regex='^[0-9]{14}$', message='SSN must be 14 numeric digits', code='invalid_ssn')], null=True)
    
    # rate = models.IntegerField(blank=True , default=0)
    REQUIRED_FIELDS = ['first_name', 'last_name']

    @classmethod
    def usersList(self):
        return self.objects.all()