# Generated by Django 3.0.2 on 2020-03-23 12:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0042_orders_seen_by_rest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviews',
            name='date',
            field=models.DateField(default=datetime.date(2020, 3, 23)),
        ),
    ]