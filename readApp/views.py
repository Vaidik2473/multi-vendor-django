from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import *
from django.http import HttpResponse
import json
import datetime
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

def store(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items
    else:
        items=[]    
        order={'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartItems=order['get_cart_items']
    products=Product.objects.all()
    context={'products':products,'cartItems':cartItems}
    return render(request,"HOME/store.html",context)
    

def Login_page(request):

    if request.method == "POST":
        username=request.POST.get("username")
        password=request.POST.get("password")

        if not User.objects.filter(username = username).exists():
            messages.error(request, "Username does not exist.")
            return redirect("/login/")
        
        user = authenticate(username = username , password = password)

        if user is None:
            messages.error(request, "Incorrect Password.")
            return redirect("/login/")



    return render(request,"HOME/login.html",context={'page':'Login'})



def logout_page(request):
    logout(request)
    return redirect("/login/")

def register(request):
    if request.method != "POST":
        return render(request,"HOME/register.html",context={'page':'register'})
    first_name=request.POST.get("first_name")
    last_name=request.POST.get("last_name")
    username=request.POST.get("username")
    password=request.POST.get("password")

    user = User.objects.filter(username = username)

    if user.exists():
        messages.error(request, "Username already taken")
        return redirect('/register/')

    user = User.objects.create(
        first_name=first_name,
        last_name=last_name,
        username=username
    )
    user.set_password(password)
    user.save()
    messages.info(request , "Account created successfully")
    return redirect('/register/')


def cart(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items
    else:
        items=[]    
        order={'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartItems=order['get_cart_items']

    context={'items':items,'order':order,'cartItems':cartItems}
    return render(request,"HOME/cart.html",context)


def checkout(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items
    else:
        items=[]    
        order={'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartItems=order['get_cart_items']

    context={'items':items,'order':order,'cartItems':cartItems}
    return render(request,"HOME/checkout.html",context)

def updateItem(request):
    data=json.loads(request.body)
    productId=data['productId']
    action=data['action']
    print('Action',action)
    print('Product',productId)
    customer=request.user.customer
    product=Product.objects.get(id=productId)
    order,created=Order.objects.get_or_create(customer=customer,complete=False)
    orderItem,created=OrderItem.objects.get_or_create(order=order,product=product)

    if action=='add':
        orderItem.quantity=(orderItem.quantity+1)
    elif action=='remove':
        orderItem.quantity=(orderItem.quantity-1)
    
    orderItem.save()

    if orderItem.quantity<=0:
        orderItem.delete()
    return JsonResponse('Item was added',safe=False)

def processOrder(request):
    transaction_id=datetime.datetime.now().timestamp()
    data=json.loads(request.body)

    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        total=float(data['form']['total'])
        order.transaction_id=transaction_id

        if total==order.get_cart_total:
            order.complete=True
        order.save()

        if order.shipping==True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['address'],
                state=data['shipping']['address'],
                zipcode=data['shipping']['address']
            )

    else:
        print('User is not logged in...')
    return JsonResponse('Payment complete',safe=False)

# from django.shortcuts import render

# def index(request):
#     return render(request, 'index.html')
