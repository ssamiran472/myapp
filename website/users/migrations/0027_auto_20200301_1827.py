# Generated by Django 3.0.2 on 2020-03-01 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0026_auto_20200301_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ratings',
            name='rate',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='restaurents',
            name='avarage_ratings',
            field=models.FloatField(default=0),
        ),
    ]
