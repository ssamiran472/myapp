# Generated by Django 3.0.2 on 2020-01-24 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200124_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippers',
            name='identy_proof',
            field=models.CharField(max_length=50),
        ),
    ]
