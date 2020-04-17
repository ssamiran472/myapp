from django.db import models
from django.contrib.auth.models import User
# from datetime import date
from django.utils import timezone
from django.db.models.signals import post_save
from django.contrib.auth.decorators import login_required
import datetime

class Restaurents(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, default=None)
    name = models.CharField(max_length=100)
    address = models.CharField(default='Bangalore',max_length=255)
    mob_no = models.CharField(max_length=12)
    city = models.CharField(max_length=50)
    country = models.CharField( max_length=50)
    pincode = models.IntegerField()
    locality = models.CharField( max_length=50, default=None )
    restaurent_Main_img= models.ImageField(upload_to='restaurent/', default='')
    avarage_ratings = models.FloatField(default=0)
    total_reviews = models.IntegerField(default=0)
    def __str__(self):
        return self.name




class Shippers(models.Model):
    shipper= models.ForeignKey(User, on_delete = models.CASCADE, to_field='id')
    name = models.CharField(max_length=50)
    mob_no = models.CharField(max_length =12)
    identy_proof = models.CharField(max_length = 50)
    photo = models.ImageField()
    deriving_licence = models.ImageField(upload_to='Shippers/', default='')
    start_duty = models.BooleanField(default=False)
    Vechile_no = models.CharField(default='', max_length=17)
    Vachile_type= models.CharField(default='', max_length=20)
    locality = models.CharField(max_length=50, default=None)
    is_in_order = models.BooleanField(default=False)
    total_order=models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Category(models.Model):
    restaurent= models.ForeignKey(Restaurents, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Foods(models.Model):
    foods_name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField(default = 00.00)
    image = models.ImageField(upload_to='food_images/', default='')
    description = models.CharField(max_length=255, default=None)
    restaurent = models.ForeignKey(Restaurents, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.foods_name

class Successfull_order(models.Manager):
    def get_queryset(self):
        return super(Successfull_order, self).get_queryset().filter(stautus=True)

STATUS_CHOICES = (
    ("O", "ORDERD"),
    ("A&P", "ACCEPT & PREPARING"),
    ("R", "REJECT"),
    ("RD", "READY FOR DELIVERY"),
    ("P&D", "PICKED UP & ON ROAD"),
    ("S", "SUCCESS"),
)
class Orders(models.Model):
    # fields..
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurents_id = models.ForeignKey(Restaurents, on_delete=models.CASCADE)
    order_date = models.DateField()
    order_date_and_time = models.DateTimeField(auto_now_add=True)
    shipper_id = models.ForeignKey(Shippers, on_delete=models.CASCADE, null=True, blank=True)
    total_price = models.IntegerField(default=0)
    stautus = models.BooleanField(default=False)
    seen_by_rest=models.BooleanField(default=False)
    accepet_by_rest=models.BooleanField(default=False)
    received_by_delivery = models.BooleanField(default=False)
    order_statuses=models.CharField(
        max_length = 20,
        choices = STATUS_CHOICES,
        default = 'O'
        )
    # Model Manager..
    objects = models.Manager() #default manager
    # Successfull_order() is a modelManager which is helped to get that orders whose payment is successfull.
    successfull_order = Successfull_order()

class Orderdetails(models.Model):
    order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)
    food_id = models.ForeignKey(Foods, on_delete=models.CASCADE)
    quentity = models.IntegerField()

    @property
    def total_cost(self):
        return self.quentity * self.food_id.price


class Ratings(models.Model):
    rate = models.IntegerField(default=0)
    coustomer_id = models.ForeignKey(User, on_delete = models.CASCADE)
    restaurents_id = models.ForeignKey(Restaurents, on_delete=models.CASCADE)

class Reviews(models.Model):
    coustomer_id = models.ForeignKey(User, on_delete = models.CASCADE)
    restaurents_id = models.ForeignKey(Restaurents, on_delete=models.CASCADE)
    comment = models.TextField()
    date= models.DateField(default=datetime.date.today())

class userAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    locality=models.CharField(default='', max_length=20)
    city=models.CharField(default='', max_length=20)
    pin = models.CharField(max_length=6)
    mob = models.CharField(max_length=10)



class communicat(models.Model):
    coustomer_id = models.ForeignKey(User, on_delete = models.CASCADE)
    restaurents_id = models.ForeignKey(Restaurents, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateField()

class user_designations(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)   
    designations = models.CharField(max_length =20, default=None)

    def __str__(self):
        return self.user.first_name

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
