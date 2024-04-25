from django.db import models

# Create your models here.
class Customer(models.Model):
    customer_name=models.CharField(max_length=50)
    customer_email=models.EmailField(unique=True,null=False)
    customer_password=models.CharField(max_length=20)

def __str__(self):
    return self.customer_name