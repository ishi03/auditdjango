from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
import json
import datetime

from .forms import CreateUserForm,Aform
from .models import *
from .models import ShippingAddress
from .utils import cartData


def loginPage(request):
    if request.method=='POST':
       username=request.POST.get('username')
       password=request.POST.get('password')
       user=authenticate(request,username=username,password=password)
       if user is not None:
           login(request,user)
           return redirect('store')
       else :
           messages.info(request,'Username or password incorrect')
    context={}
    return render(request,'store/login.html',context)


def registerPage(request):
    form=CreateUserForm
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'account created')
            return redirect('login')
    context={
        "form":form,
    }
    return render(request,'store/register.html',context)

def SubmitPage(request):
    
    return render(request,'store/checkout.html',context)


def logoutUser(request):
    logout(request)
    return redirect('login')

def store(request):
	data = cartData(request)
	cartItems = data['cartItems']
	products = Product.objects.all()
	context = {'products': products, 'cartItems': cartItems}
	return render(request, 'store/store.html', context)

def description(request,pk):
	queryset = Product.objects.get(id=pk)
	context = {'queryset':queryset}
	return render(request, 'store/description.html',context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	print('In cart')

	context = {'items': items, 'order': order, 'cartItems': cartItems}
	return render(request, 'store/cart.html', context)


def checkout1(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	form=Aform()
	if request.method=='POST':
		form=Aform(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request,'order confirmed')
			return redirect('store')
	context={"form":form, 'items': items, 'order': order, 'cartItems': cartItems}
	return render(request, 'store/checkout.html', context)

def checkout(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	context={'items': items, 'order': order, 'cartItems': cartItems}
	if request.method == 'POST':
		if  request.POST.get('address') and request.POST.get('city') and request.POST.get('state') and request.POST.get('zipcode'):
			post=ShippingAddress()
			#post.customer= request.POST.get('customer')
			post.address = request.POST.get('address')
			post.city = request.POST.get('city')
			post.state = request.POST.get('state')
			post.zipcode = request.POST.get('zipcode')
			post.order = order
			post.save()
			#messages.success(request,'order confirmed')
			return render(request, 'store/congrats.html',context)
		else:
			return redirect('cart')
	else:
		
		return render(request,'store/checkout.html',context)


def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)





