# Generated by Django 3.0.2 on 2020-03-20 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0041_auto_20200320_1017'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='seen_by_rest',
            field=models.BooleanField(default=False),
        ),
    ]
