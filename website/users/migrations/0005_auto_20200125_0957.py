# Generated by Django 3.0.2 on 2020-01-25 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200125_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurents',
            name='address',
            field=models.CharField(default='Bangalore', max_length=255),
        ),
    ]
