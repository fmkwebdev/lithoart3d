from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.http import JsonResponse, HttpResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder
from .models import OrderConfirmation
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext as _

def confirmation_page(request):
    if not request.session.get('purchased', False):
        return redirect('unauthorized') 
    if request.method == 'POST':
        confirmation_number = request.POST.get('confirmation_number')
        name = request.POST.get('name')
        email = request.POST.get('email')
        file = request.FILES.get('file')
        confirmation = OrderConfirmation(
            confirmation_number=confirmation_number,
            name=name,
            email=email,
            file=file
        )
        confirmation.save()

        return redirect('confirmation_success')  # Redirect to a success page
    else:
        confirmation_number = get_random_string(length=5, allowed_chars='1234567890')
        return render(request, 'store/dynamic.html', {'confirmation_number': confirmation_number})


def confirmation_page_sr(request):
    if not request.session.get('purchased', False):
        return redirect('unauthorized') 
    if request.method == 'POST':
        confirmation_number = request.POST.get('confirmation_number')
        name = request.POST.get('name')
        email = request.POST.get('email')
        file = request.FILES.get('file')
        confirmation = OrderConfirmation(
            confirmation_number=confirmation_number,
            name=name,
            email=email,
            file=file
        )
        confirmation.save()

        return redirect('confirmation_success')  # Redirect to a success page
    else:
        confirmation_number = get_random_string(length=5, allowed_chars='1234567890')
        return render(request, 'store/sr/dynamic.html', {'confirmation_number': confirmation_number})
def confirmation_success(request):
    request.session['purchased'] = False
    return redirect('store')

def paymentComplete(request):
    
    body = json.loads(request.body)
    print('BODY:', body)
    product = Product.objects.get(id=body['productId'])
    Order.objects.create(
    product=product
    )
    return JsonResponse('Payment Completed', safe=False)



def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)

def storesr(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'store/sr/store.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def cartsr(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	products = Product.objects.values('id', 'name', 'name2', 'price')
	context = {'products':products,'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/sr/cart.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	products = Product.objects.all()
	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def checkoutsr(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	products = Product.objects.all()
	context = {'products':products, 'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/sr/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId, name=product.name, serbian_name=product.serbian_name)
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

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt

def processOrder(request):
    request.session['purchased'] = True
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
        order.save()
    if order.shipping == True:
        ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        zipcode=data['shipping']['zipcode'],
        )
    return JsonResponse('Payment submitted..', safe=False)

def pay(request):
	return render(request, 'store/pay.html')

def unauthorized(request):
    return render(request, 'store/unauthorized.html')


