from django.shortcuts import render, redirect, HttpResponse
from .models import Product, Customer, Order

import json

def index(request):
	context = {
	
	}
	return render(request, 'index.html', context)

def product(request, product_id):
	try:
		context = {
			'product': Product.get_product_by_id(product_id),
		}
		return render(request, 'product.html', context)
	except Exception as e:
		return render(request, 'error.html', { 'error': f"{e}", 'msg': "Something went wrong, try again later" })

def categories(request, category):
	_category = category.capitalize()
	try:
		context = {
			'category': _category,
			'products': Product.get_products_by_category(_category),
		}
		return render(request, 'categories.html', context)
	except Exception as e:
		return render(request, 'error.html', { 'error': f"{e}", 'msg': "Something went wrong, try again later" })

def search(request):
	query = request.GET['q']
	_q = query.split(" ")

	try:
		context = {
			'products': Product.search_product(_q),
			'query': query,
		}
		return render(request, 'search.html', context)
	except Exception as e:
		return render(request, 'error.html', { 'error': f"{e}", 'msg': "Something went wrong, try again later" })

def user(request):
	try:
		if 'username' in request.session:
			context = {
				'username' : request.session['username'],
				'password' : request.session['password'],
				'fname' : request.session['fname'],
				'lname' : request.session['lname'],
				'phno' : request.session['phno'],
				'address' : request.session['address'],
			}
			return render(request, 'profile.html', context)
		else:
			return render(request, 'login.html')
	except Exception as e:
		return render(request, 'error.html', { 'error': f"{e}", 'msg': "Something went wrong, try again later" })

def remove_user(request, _username):
	try:
		user = Customer.get_customer_by_username(_username)
		user.delete()
		return redirect('logout')
	except Exception as e:
		return render(request, 'error.html', { 'error': f"{e}", 'msg': "Something went wrong, try again later" })

def login(request):
	username = request.GET['username']
	password = request.GET['password']

	try:
		customer = Customer.get_customer_by_username(username)

		if customer and customer.password == password:
			request.session['username'] = username
			request.session['password'] = password
			request.session['fname'] = customer.first_name
			request.session['lname'] = customer.last_name
			request.session['phno'] = customer.phno
			request.session['address'] = customer.address
			return redirect('user')
		else:
			return render(request, 'error.html', { 'error': "Check username and password", 'msg': "Username or password does not match" })
	except Exception as e:
		return render(request, 'error.html', { 'error': f"{e}", 'msg': "Could not Login, Check whether cookies are turned on" })

def logout(request):
	try:
		del request.session['username'];
		del request.session['password'];
		del request.session['fname'];
		del request.session['lname'];
		del request.session['phno'];
		del request.session['address'];

		return redirect('user')
	except Exception as e:
		return render(request, 'error.html', { 'error': f"{e}", 'msg': "Something went wrong, Check whether cookies are turned on" })

def register(request):
	return render(request, 'register.html')

def add_user(request):
	try:
		username = request.POST['username']
		password = request.POST['password']
		fname = request.POST['fname']
		lname = request.POST['lname']
		phno = request.POST['phno']
		address = request.POST['address']
		c = Customer(username=username, password=password, first_name=fname, last_name=lname, phno=phno, address=address)
		c.save()
		request.session['username'] = c.username
		request.session['password'] = c.password
		request.session['fname'] = c.first_name
		request.session['lname'] = c.last_name
		request.session['phno'] = c.phno
		request.session['address'] = c.address
		return redirect('user')
	except Exception as e:
		return render(request, 'error.html', { 'error': f"{e}", 'msg': "Could not register, Check whether cookies are turned on" })

def add_to_wishlist(request, product_id):
	try:
		if 'username' in request.session:
			user = Customer.get_customer_by_username(request.session['username'])
			wishlist = json.loads(user.wishlist)
			wishlist[product_id] = 0
			user.wishlist = json.dumps(wishlist)
			user.save(update_fields=["wishlist"])
			return redirect('wishlist')
		else:
			return redirect('user')
	except Exception as e:
		return render(request, 'error.html', { 'error': f"{e}", 'msg': "Something went wrong, try again later" })

def remove_from_wishlist(request, product_id):
	try:
		if 'username' in request.session:
			user = Customer.get_customer_by_username(request.session['username'])
			wishlist = json.loads(user.wishlist)
			wishlist.pop(str(product_id))
			user.wishlist = json.dumps(wishlist)
			user.save(update_fields=["wishlist"])
			return redirect('wishlist')
		else:
			return redirect('user')
	except Exception as e:
		return render(request, 'error.html', { 'error': f"{e}", 'msg': "Something went wrong, try again later" })		

def wishlist(request):
	try:
		if 'username' in request.session:
			user = Customer.get_customer_by_username(request.session['username'])
			wishlist = json.loads(user.wishlist)
			wishlist = list(wishlist)
			products = Product.get_products_by_id(wishlist)
			return render(request, 'wishlist.html', { 'products': products })
		else:
			return redirect('user')
	except Exception as e:
		return render(request, 'error.html', { 'error': f"{e}", 'msg': "Something went wrong, try again later" })

def cart(request):
	try:
		cart = request.COOKIES.get('cart', '{}')
		cart = json.loads(cart)

		cart_items = []
		total_amount = 0

		for product_id, qty in cart.items():
			product = Product.objects.get(id=product_id)
			item_total = product.price * qty
			total_amount += item_total
			cart_items.append({'product': product, 'qty': qty, 'item_total': item_total})

		context = {
			'cart_items': cart_items,
			'total_amount': total_amount,
		}
		return render(request, 'cart.html', context)
	except Exception as e:
		return render(request, 'error.html', { 'error': f"{e}", 'msg': "Something went wrong, try again later" })

def update_cart(request):
	try:
		product_id = request.GET['id']
		qty = request.GET['qty']

		cart = request.COOKIES.get('cart', '{}')
		cart = json.loads(cart)
		cart[str(product_id)] = int(qty)

		response = redirect('cart')
		response.set_cookie('cart', json.dumps(cart))
		return response
	except Exception as e:
		return render(request, 'error.html', { 'error': f"{e}", 'msg': "Could not add to cart, try again later" })

def remove_from_cart(request, product_id):
	try:
		cart = request.COOKIES.get('cart', '{}')
		cart = json.loads(cart)

		cart.pop(str(product_id))

		response = redirect('cart')
		response.set_cookie('cart', json.dumps(cart))
		return response
	except Exception as e:
		return render(request, 'error.html', { 'error': f"{e}", 'msg': "Something went wrong, try again later" })

def checkout(request):
	try:
		cart = request.COOKIES.get('cart', '{}')
		cart = json.loads(cart)

		cart_items = []
		total_amount = 0

		for product_id, qty in cart.items():
			product = Product.objects.get(id=product_id)
			item_total = product.price * qty
			total_amount += item_total
			cart_items.append({'product': product, 'qty': qty, 'item_total': item_total})

		context = {
			'cart_items': cart_items,
			'total_amount': total_amount,
		}
		if 'username' in request.session:
			return render(request, 'checkout.html', context)
		else:
			return redirect('user')
	except Exception as e:
		return render(request, 'error.html', { 'error': f"{e}", 'msg': "Something went wrong, try again later" })

def place_order(request):
	try:
		if request.method == 'POST':
			fname = request.POST['fname']
			lname = request.POST['lname']
			uname = request.POST['uname']
			email = request.POST['email']
			phno = request.POST['phno']
			address = request.POST['address']
			amount = request.POST['amount']

		if uname == request.session['username']:
			order = Order(first_name=fname, last_name=lname, username=uname, phno=phno, email=email, address=address, amount=amount)
			order.save()
			
			response = redirect('orders')
			response.delete_cookie('cart')
			return response
		else:
			return render(request, 'error.html', { 'error': "Invalid Username", 'msg': "Enter Valid username" })
	except Exception as e:
		return render(request, 'error.html', { 'error': f"{e}", 'msg': "Something went wrong, try again later" })

def orders(request):
	try:
		if 'username' in request.session:
			username = request.session['username']
			context = {
				'orders': Order.get_orders_by_username(username),
			}
			return render(request, 'orders.html', context)
		else:
			return redirect('user')
	except Exception as e:
		return render(request, 'error.html', { 'error': f"{e}", 'msg': "Something went wrong, try again later" })

def cancel_order(request, id):
	try:
		order = Order.get_order_by_id(id)
		order.status = Order.STATUS[3][0]
		order.save(update_fields=["status"])
		return redirect('orders')
	except Exception as e:
		return render(request, 'error.html', { 'error': f"{e}", 'msg': "Something went wrong, try again later" })
