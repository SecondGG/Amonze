from audioop import reverse
from http.client import HTTPResponse
from multiprocessing import context
import re
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from app_amonze.models import Customer, Item, Transaction, TransactionItem, ShippingAddress
from app_amonze.forms import SignUpForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from app_amonze.forms import ProfileForm, CustomerForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
import json


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

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('marketplace')
        else:
            messages.info(request, 'Username or password is in correct.')

    context = {}
    return render(request, 'login.html', context)   

def logoutUser(request):
    logout(request)
    return redirect('login')

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = SignUpForm()
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Account created')
                return redirect('login')

    context = {'form':form}
    return render(request, 'signup.html', context)

"""def ProfilePage(request): 
    instance = get_object_or_404(Customer, user=request.user)
    form = ProfileForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('home')
    else:
        context = {
            'form':form,
            'user':request.user
            }
        return render(request, 'profile.html', context) """
    
def profile(request):
    customer = request.user.customer 
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context={'form':form}
    return render(request, 'profile.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        transactions, created = Transaction.objects.get_or_create(customer=customer, complete = False)
        items = TransactionItem.objects.filter(transaction=transactions)
    else:
        items = []
    context = {'items':items, 'transaction':transactions}
    return render(request, 'cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        transactions, created = Transaction.objects.get_or_create(customer=customer, complete = False)
        items = TransactionItem.objects.filter(transaction=transactions)
    else:
        items = []
    context = {'items':items, 'transaction':transactions}
    return render(request, 'checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    itemId = data['itemId']
    action = data['action']

    print('Action:', action)
    print('itemId:', itemId)

    customer = request.user.customer
    item = Item.objects.get(item_id=itemId)
    transactions, created = Transaction.objects.get_or_create(customer=customer, complete = False)
    transactionItems, created = TransactionItem.objects.get_or_create(transaction=transactions, item=item)
    
    if action == 'add':
        transactionItems.quantity = (transactionItems.quantity + 1)
    elif action == 'remove':
        transactionItems.quantity = (transactionItems.quantity - 1)
    
    transactionItems.save()

    if transactionItems.quantity <= 0:
        transactionItems.delete()
    
    return JsonResponse('Item was added', safe=False)