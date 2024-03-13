from django.db import models
from order.models import Order

import datetime
class Payment(models.Model):
  date = models.DateField(default=datetime.datetime.today)
  method = models.CharField(max_length=50)
  status = models.BooleanField(default=False)

class PaymentOrder(models.Model):
  payment_id=models.ForeignKey(Payment,on_delete=models.CASCADE)
 
class PaymentVendor(models.Model):
  payment_id=models.ForeignKey(Payment, on_delete=models.CASCADE)
  plan=models.TextField(max_length=1000)