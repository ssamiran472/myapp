# Generated by Django 3.0.2 on 2020-03-20 10:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0040_auto_20200319_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviews',
            name='date',
            field=models.DateField(default=datetime.date(2020, 3, 20)),
        ),
    ]