import imp
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User

class Customer (models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    customer_id = models.BigAutoField(primary_key=True)
    firstname = models.CharField(max_length=50, null=True)
    lastname = models.CharField(max_length=50, null=True)
    date_of_birth = models.DateField(null=True)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=100,null=True)
    postcode = models.CharField(max_length=5,null=True)
    profile_pic = models.ImageField(default="default_profile_pic.png",null=True, blank=True)
    def __str__(self):
        return "%s %s %s"%(self.pk, self.user, self.firstname)

class Item (models.Model):
    item_id = models.BigAutoField(primary_key=True)
    item_name = models.CharField(max_length=50)
    item_image = models.ImageField(null=True)
    description = models.TextField(default="No description")
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    def __str__(self):
        return "%s %s"%(self.pk, self.item_name)

class Transaction (models.Model):
    transaction_id = models.BigAutoField(primary_key=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True)
    item = models.ForeignKey('Item', on_delete=models.CASCADE, null=True)
    subtotal = models.PositiveIntegerField()
    datetime = models.DateTimeField(auto_now_add=True)