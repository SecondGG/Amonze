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
        transaction, created = Transaction.objects.get_or_create(customer=customer, complete = False)
        items = transaction.objects.all()
    else:
        items = []
    context = {'items':items}
    return render(request, 'cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'checkout.html', context)