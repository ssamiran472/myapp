# Generated by Django 3.0.2 on 2020-03-14 13:05

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0034_auto_20200314_0938'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='orders',
            managers=[
                ('successfull_order', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='orders',
            name='stautus',
            field=models.BooleanField(default=False),
        ),
    ]
