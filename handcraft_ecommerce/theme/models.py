from django.db import models

# Create your models here.
class Cars(models.Model):
    x=[
        ("KIA","KIA"),
        ("BMW","BMW"),
        ("BYD","BYD"),
        ("GEELY","GEELY"),
    ]
    name=models.CharField(max_length=100)
    prise=models.IntegerField()
    Categories=models.CharField(max_length=100,null=True,choices=x)

    def __str__(self):
        return self.name