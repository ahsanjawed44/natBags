# Generated by Django 4.2.3 on 2024-04-22 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('News', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='news_date',
            field=models.DateField(default="2024-12-05"),
        ),
        migrations.AddField(
            model_name='news',
            name='news_desc',
            field=models.TextField(default='None', max_length=500),
        ),
        migrations.AddField(
            model_name='news',
            name='news_img',
            field=models.ImageField(default='None', upload_to=''),
        ),
        migrations.AddField(
            model_name='news',
            name='news_title',
            field=models.CharField(default='None', max_length=50),
        ),
    ]