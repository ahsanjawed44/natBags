from django.contrib import admin
from Shop.models import *

# Register your models here.
class shopAdmin(admin.ModelAdmin):
    list_display=['product_name','product_price','product_quantity','product_catagory']

admin.site.register(product,shopAdmin)

class catagoryAdmin(admin.ModelAdmin):
    list_display=['catagory_name']

admin.site.register(catagory,catagoryAdmin)

class cartAdmin(admin.ModelAdmin):
    list_display=['Customer']

admin.site.register(cart)

class cartItemAdmin(admin.ModelAdmin):
    list_display=['cartF','productF','quantity']

admin.site.register(cartItems,cartItemAdmin)


class feedbackAdmin(admin.ModelAdmin):
    list_display=['userid','productid','rating', 'date']

admin.site.register(review_product,feedbackAdmin)