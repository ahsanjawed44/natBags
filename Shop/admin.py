from django.contrib import admin
from Shop.models import *

# Register your models here.
class shopAdmin(admin.ModelAdmin):
    list_display=['product_name','product_price','product_quantity','product_catagory','product_rating']

admin.site.register(product,shopAdmin)

class catagoryAdmin(admin.ModelAdmin):
    list_display=['catagory_name']

admin.site.register(catagory,catagoryAdmin)

class cartAdmin(admin.ModelAdmin):
    list_display=['id','Customer','is_paid']

admin.site.register(cart,cartAdmin)

class cartItemAdmin(admin.ModelAdmin):
    list_display=['id','cartF','productF','quantity']

admin.site.register(cartItems,cartItemAdmin)

class orderAdmin(admin.ModelAdmin):
    list_display=['id','customer_name','customer_email','total_bill','phone','date']

admin.site.register(orderModel,orderAdmin)

class feedbackAdmin(admin.ModelAdmin):
    list_display=['userid','productid','rating', 'date']

admin.site.register(review_product,feedbackAdmin)