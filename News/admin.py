from django.contrib import admin
from News.models import news

# Register your models here.
class newsAdmin(admin.ModelAdmin):
    list_display=['news_title','news_img','news_date','posted_by']

admin.site.register(news,newsAdmin)