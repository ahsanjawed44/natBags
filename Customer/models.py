from django.db import models
from django.conf import settings
import uuid
# Create your models here.
class Customer(models.Model):
    customer_name=models.CharField(max_length=50)
    customer_email=models.EmailField(unique=True,null=False)
    customer_password=models.CharField(max_length=20)
    is_verified = models.BooleanField(default=False)  # New field for email verification
    email_token = models.UUIDField(default=uuid.uuid4, editable=False)

def __str__(self):
    return self.customer_name




