# Generated by Django 4.2.3 on 2024-05-08 18:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0001_initial'),
        ('Shop', '0009_rename_user_cart_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='review_product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField(max_length=1000)),
                ('rating', models.CharField(default='0', max_length=10)),
                ('date', models.DateField(auto_now_add=True)),
                ('productid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Shop.product')),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Customer.customer')),
            ],
        ),
    ]
