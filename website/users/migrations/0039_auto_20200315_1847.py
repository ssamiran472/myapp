# Generated by Django 3.0.2 on 2020-03-15 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0038_auto_20200315_1812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='order_date_and_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
