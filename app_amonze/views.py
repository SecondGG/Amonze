from django.shortcuts import render
from django.http.response import HttpResponse

# Create your views here.
def home(request):
    return render(request, 'home.html')

def marketplace(request):
    return render(request, 'marketplace.html')

def item(request, item_id):
    return render(request, 'item.html', context={'item_id': item_id})