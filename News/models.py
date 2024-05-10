from django.db import models
from django.utils import timezone


# Create your models here.
class news(models.Model):
    news_title = models.CharField(max_length=50, default='')
    news_desc = models.TextField(max_length=1500, default='')
    news_img = models.ImageField(upload_to='news',null=False, default='None')
    news_date = models.DateField(default=timezone.now)  # Use auto_now_add to set the date automatically
    posted_by = models.CharField(max_length=20, default='Admin')
    # news_comments=models.ForeignKey(comments,on_delete=models.CASCADE)


def __str__(self):
    return self.news_title


# class news_comment(models.Model):
#     comment=models.TextField(max_length=500)
    