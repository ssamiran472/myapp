# Generated by Django 3.0.2 on 2020-01-25 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20200125_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurents',
            name='password',
            field=models.CharField(default='email', max_length=10),
        ),
    ]
