from urllib import response
from django.shortcuts import render, redirect
from app_amonze.models import *
from app_amonze.forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import  redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
import json
import urllib.request



# Create your views here.
def home(request):
    return render(request, 'home.html')


def marketplace(request):
    items = Item.objects.all()
    context = {'items': items}
    return render(request, 'marketplace.html', context)


def item(request, item_id):
    item = Item.objects.get(item_id=item_id)
    context = {'item': item}
    return render(request, 'item.html', context)

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.info(request, 'Username or password is in correct.')

    context = {}
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


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

    context = {'form': form}
    return render(request, 'signup.html', context)



@login_required(login_url='login')
def profile(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    context = {'form': form}
    return render(request, 'profile.html', context)


@login_required(login_url='login')
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        transactions, created = Transaction.objects.get_or_create(
            customer=customer, complete=False)
        items = TransactionItem.objects.filter(transaction=transactions)
    else:
        items = []
        transactions = {'get_cart_total': 0, 'shipping': False}
    context = {'items': items, 'transaction': transactions}
    return render(request, 'cart.html', context)


@login_required(login_url='login')
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        transactions, created = Transaction.objects.get_or_create(
            customer=customer, complete=False)
        items = TransactionItem.objects.filter(transaction=transactions)
        if len(items) == 0:
            return redirect('cart')
    else:
        items = []
        transactions = {'get_cart_total': 0, 'shipping': False}
    context = {'items': items, 'transaction': transactions}
    return render(request, 'checkout.html', context)


@login_required(login_url='login')
def updateItem(request):
    data = json.loads(request.body)
    itemId = data['itemId']
    action = data['action']

    print('Action:', action)
    print('itemId:', itemId)

    customer = request.user.customer
    item = Item.objects.get(item_id=itemId)
    transactions, created = Transaction.objects.get_or_create(
        customer=customer, complete=False)
    transactionItems, created = TransactionItem.objects.get_or_create(
        transaction=transactions, item=item)

    if action == 'add':
        transactionItems.quantity = (transactionItems.quantity + 1)
    elif action == 'remove':
        transactionItems.quantity = (transactionItems.quantity - 1)

    detail = {
        "itemId" : itemId,
        "aciton" : action,
        "quantity" : transactionItems.quantity,
    }

    dictionary = {"detail": detail}
    json_object = json.dumps(dictionary)
    print(json_object)
    response = redirect('marketplace')
    response.set_cookie('amonze_cart', json_object)

    transactionItems.save()

    if transactionItems.quantity <= 0:
        transactionItems.delete()

    #return JsonResponse('Item was added.', safe=False)
    return response


@login_required(login_url='login')
def processOrder(request):
    print('Data:', request.body)
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        transactions, created = Transaction.objects.get_or_create(
            customer=customer, complete=False)
        total = float(data['form']['total'])

        if total == transactions.get_cart_total:
            transactions.complete = True
        transactions.save()
    return JsonResponse('Payment Completed', safe=False)


@login_required(login_url='login')
def owned(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        transactions = Transaction.objects.filter(
            customer=customer, complete=True)
        items = TransactionItem.objects.filter(transaction__in=transactions)

        p = Paginator(items, 12)
        
        page_num = request.GET.get('page', 1)
        try:
            page = p.page(page_num)
        except:
            page = p.page(1)
    else:
        items = []
        transactions = {'get_cart_total': 0}
    context = {'items': page, 'transaction': transactions}
    return render(request, 'owned.html', context)


@login_required(login_url='login')
def eth_pay(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        transactions = Transaction.objects.get(
            customer=customer, complete=False)
    else:
        transactions = {'get_cart_total':0, 'shipping':False}
    context = {'transaction':transactions}
    return render(request, 'eth_pay.html', context)


from django.http import HttpResponse
from PIL import Image
import libscrc
import qrcode


def calculate_crc(code):
    crc = libscrc.ccitt_false(str.encode(code))
    crc = str(hex(crc))
    crc = crc[2:].upper()
    return crc.rjust(4, '0')


def gen_code(mobile="", nid="", amount=1.23):
    code="00020101021153037645802TH29370016A000000677010111"
    if mobile:
        tag,value = 1,"0066"+mobile[1:]
        seller='{:02d}{:02d}{}'.format(tag,len(value), value)
    elif nid:
        tag,value = 2,nid
        seller='{:02d}{:02d}{}'.format(tag,len(value), value)
    else:
        raise Exception("Error: gen_code() does not get seller mandatory details")
    code+=seller
    tag,value = 54, '{:.2f}'.format(amount)
    code+='{:02d}{:02d}{}'.format(tag,len(value), value)
    code+='6304'
    code+=calculate_crc(code)
    return code


def get_qr(request,mobile="",nid="",amount=""):
    message="mobile: %s, nid: %s, amount: %s"%(mobile,nid,amount)
    print( message )
    code=gen_code(mobile=mobile, amount=float(amount))#scb
    print(code)
    img = qrcode.make(code,box_size=4)
    response = HttpResponse(content_type='image/png')
    img.save(response, "PNG")
    return response

@login_required(login_url='login')
def promptpay(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        transactions = Transaction.objects.get(
            customer=customer, complete=False)
        items = TransactionItem.objects.filter(transaction=transactions)
        form = EvidenceForm(instance=transactions)
        if request.method == 'POST':
            form = EvidenceForm(request.POST, request.FILES, instance=transactions)
            if form.is_valid():
                form.save()
    else:
        items = []
        transactions = {'get_cart_total':0, 'shipping':False}
    context = {'transaction':transactions}
    context={
        "mobile":"0845552363", #seller's mobile
        'amount': transactions.get_cart_total*34,
        'transaction':transactions,
        'items': items,
        'form': form,
    }
    return render(request, 'promptpay.html', context)

