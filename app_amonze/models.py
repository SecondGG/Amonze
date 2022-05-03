import imp
from itertools import product
from django.db import models
from django.contrib.auth.models import User

class Customer (models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    customer_id = models.BigAutoField(primary_key=True)
    profile_pic = models.ImageField(default="default_profile_pic.png",null=True, blank=True)
    firstname = models.CharField(max_length=50, null=True, blank=True)
    lastname = models.CharField(max_length=50, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    address = models.CharField(max_length=300,null=True, blank=True)
    postcode = models.CharField(max_length=5,null=True, blank=True)
    
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
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    evidence = evidence = models.ImageField(null=True, blank=True)

    def __str__(self):
        return "%s"%(self.pk)

    @property
    def get_cart_total(self):
        transactionitems = self.transactionitem_set.all()
        total = sum([item.get_total for item in transactionitems])
        return total

class TransactionItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    @property
    def get_total(self):
        total = self.item.price * self.quantity
        return total