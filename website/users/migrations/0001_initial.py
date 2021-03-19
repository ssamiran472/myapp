# Generated by Django 3.0.2 on 2020-01-23 15:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Foods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foods_name', models.CharField(max_length=50)),
                ('price', models.FloatField()),
                ('image', models.ImageField(upload_to='')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Restaurents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('mob_no', models.IntegerField()),
                ('city', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('pincode', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Shippers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('mob_no', models.IntegerField()),
                ('identy_proof', models.TextField()),
                ('photo', models.ImageField(upload_to='')),
                ('delivery_licence', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Ratings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.IntegerField()),
                ('comment', models.CharField(max_length=100)),
                ('coustomer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('foods_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Foods')),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateField()),
                ('restaurents_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Restaurents')),
                ('shipper_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Shippers')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Orderdetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quentity', models.IntegerField()),
                ('food_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Foods')),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Orders')),
            ],
        ),
        migrations.AddField(
            model_name='foods',
            name='restaurent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Restaurents'),
        ),
    ]