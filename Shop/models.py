from django.db import models

from Customer.models import Customer

class catagory(models.Model):
    catagory_name=models.CharField(max_length=50)

    def __str__(self):
        return self.catagory_name





class product(models.Model):
    product_name=models.CharField(max_length=50)
    product_price=models.IntegerField(default=0)
    product_image=models.ImageField(upload_to='products',default='')
    product_material=models.CharField(max_length=50,default='')
    product_details=models.TextField(max_length=1500)
    product_rating=models.IntegerField(default=0)
    product_quantity=models.IntegerField(default=0)
    product_catagory=models.ForeignKey(catagory, on_delete=models.CASCADE, null=False, default='')
    # product_reviews=models.ForeignKey
    
    def __str__(self):
        return self.product_name


class review_product(models.Model):
    userid=models.ForeignKey(Customer,on_delete=models.CASCADE,null=False)    
    productid=models.ForeignKey(product,on_delete=models.CASCADE,null=False)
    review=models.TextField(max_length=1000)
    rating=models.CharField(max_length=10, default='0')
    date=models.DateField(auto_now_add=True)

class cart(models.Model):
    Customer=models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='cart')
    is_paid=models.BooleanField(default=False)
    delivery_price=150

    def get_cart_subtotal(self):
            cart_items = self.cart_items.all()  # Assuming you have a related_name set for the cart_items ForeignKey
            subtotal_price = []
            for ci in cart_items:
                subtotal_price.append(ci.get_product_price())
            return sum(subtotal_price)
     

    def get_total(self):
        subtotal=self.get_cart_subtotal()
        
        total=subtotal + self.delivery_price
        return (total)
    
    
    
    def __str__(self):
        return self.Customer.customer_name



class cartItems(models.Model):
    cartF=models.ForeignKey(cart,on_delete=models.CASCADE,related_name='cart_items')
    productF=models.ForeignKey(product,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(default=1)

    def get_product_price(self):
        product_price=self.productF.product_price
        qty=self.quantity
        global total_price; 
        total_price= product_price * qty
        return total_price
    

    def __str__(self):
        return self.productF.product_name

# Create your models here.
