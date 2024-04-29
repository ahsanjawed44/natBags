from django.db import models

from Customer.models import Customer

class catagory(models.Model):
    catagory_name=models.CharField(max_length=50)

    def __str__(self):
        return self.catagory_name
    def save(self, *args, **kwargs):
        # Strip whitespace from category_name before saving
        self.catagory_name = self.catagory_name.strip()
        super().save(*args, **kwargs)
# class commments(models.Model):
#     pro_comments=models.TextField(max_lenght=500)

class product(models.Model):
    product_name=models.CharField(max_length=50)
    product_price=models.IntegerField(default=0)
    product_image=models.ImageField(upload_to='products',default='')
    product_material=models.CharField(max_length=50,default='')
    product_details=models.TextField(max_length=1500)
    product_rating=models.IntegerField(default=0)
    product_quantity=models.IntegerField(default=0)
    product_catagory=models.ForeignKey(catagory, on_delete=models.CASCADE, null=False, default='')
    # product_comment=models.ForeignKey



    def __str__(self):
        return self.product_name

# Create your models here.
