from django.contrib import admin
from Customer.models import Customer

# Register your models here.
class customerAdmin(admin.ModelAdmin):
    list_display=['customer_name','customer_email']

admin.site.register(Customer,customerAdmin)