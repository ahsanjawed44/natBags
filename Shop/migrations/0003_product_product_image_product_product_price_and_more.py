# Generated by Django 4.2.3 on 2024-04-29 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0002_product_product_material'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_image',
            field=models.ImageField(default='', upload_to='../Media/products'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='product_quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='product_rating',
            field=models.IntegerField(default=0),
        ),
    ]
