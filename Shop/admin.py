from django.contrib import admin
from Shop.models import *

# Register your models here.
class shopAdmin(admin.ModelAdmin):
    list_display=['product_name','product_price','product_quantity','product_catagory']

admin.site.register(product,shopAdmin)

class catagoryAdmin(admin.ModelAdmin):
    list_display=['catagory_name']

admin.site.register(catagory,catagoryAdmin)