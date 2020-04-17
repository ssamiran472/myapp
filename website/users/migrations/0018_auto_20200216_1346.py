# Generated by Django 3.0.2 on 2020-02-16 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_foods_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurents',
            name='restaurent_Main_img',
            field=models.ImageField(default='', upload_to='restaurent/'),
        ),
        migrations.AlterField(
            model_name='shippers',
            name='deriving_licence',
            field=models.ImageField(default='', upload_to='Shippers/'),
        ),
    ]
