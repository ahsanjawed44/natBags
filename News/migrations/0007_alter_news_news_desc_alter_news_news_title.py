# Generated by Django 4.2.3 on 2024-04-24 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('News', '0006_alter_news_news_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='news_desc',
            field=models.TextField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='news',
            name='news_title',
            field=models.CharField(default='', max_length=50),
        ),
    ]