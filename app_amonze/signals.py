from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Customer
from django.core.exceptions import ObjectDoesNotExist

@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_customer(sender, instance, created, **kwargs):
    try:
        instance.customer.save()
    except ObjectDoesNotExist:
        Customer.objects.create(user=instance)
