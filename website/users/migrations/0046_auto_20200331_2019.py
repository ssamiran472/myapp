# Generated by Django 3.0.2 on 2020-03-31 20:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0045_auto_20200324_1834'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippers',
            name='start_duty',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='date',
            field=models.DateField(default=datetime.date(2020, 3, 31)),
        ),
    ]
