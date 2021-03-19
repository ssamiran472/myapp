# Generated by Django 3.0.2 on 2020-03-15 18:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0036_auto_20200314_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='order_date_and_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 15, 18, 11, 29, 357237)),
        ),
        migrations.AlterField(
            model_name='communicat',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='date',
            field=models.DateField(),
        ),
    ]