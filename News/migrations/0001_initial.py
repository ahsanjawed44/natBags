# Generated by Django 4.2.3 on 2024-04-07 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='news',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posted_by', models.CharField(default='Admin', max_length=20)),
            ],
        ),
    ]