from audioop import reverse
from http.client import HTTPResponse
from django.shortcuts import render
from django.http.response import HttpResponse
from app_amonze.models import Item

# Create your views here.
def home(request):
    return render(request, 'home.html')

def marketplace(request):
    items = Item.objects.all()
    context = { 'items':items }
    return render(request, 'marketplace.html', context)

def item(request, item_id):
    item = Item.objects.get(item_id=item_id)
    context={'item': item}
    return render(request, 'item.html', context)

def register(request):
    return render(request, 'register.html')
    

def register_detail(request):
    return render(request, 'register_detail.html')    

def login(request):
    return login(request, 'login.html')   