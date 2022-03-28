from django.db import models

class Customer (models.Model):
    customer_id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=20)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    email = models.EmailField()
    address = models.CharField(max_length=100)
    postcode = models.CharField(max_length=5)
    def __str__(self):
        return "%s %s %s"%(self.pk, self.username, self.firstname)

class Item (models.Model):
    item_id = models.BigAutoField(primary_key=True)
    item_name = models.CharField(max_length=50)
    item_image = models.ImageField(null=True)
    description = models.TextField(default="No description")
    price = models.PositiveIntegerField()
    def __str__(self):
        return "%s %s"%(self.pk, self.item_name)

class Transaction (models.Model):
    transaction_id = models.BigAutoField(primary_key=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True)
    item = models.ForeignKey('Item', on_delete=models.CASCADE, null=True)
    subtotal = models.PositiveIntegerField()
    datetime = models.DateTimeField(auto_now_add=True)