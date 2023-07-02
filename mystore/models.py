from django.db import models

class Product(models.Model):
	CATEGORIES = [
		("Action", "ACTION"),
		("Mystery", "MYSTERY"),
		("Fantasy", "FANTASY"),
		("Fiction", "FICTION"),
		("Literature", "LITERATURE"),
		("Novel", "NOVEL"),
	]
	id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=50)
	author = models.CharField(max_length=50)
	imgurl = models.CharField(max_length=200, null=True)
	category = models.CharField(max_length=50, choices=CATEGORIES)
	description = models.TextField(null=True)
	price = models.FloatField()

	def get_all_products():
		return Product.objects.all()

	def get_products_by_category(_category):
		return Product.objects.filter(category=_category)

	def get_product_by_id(_id):
		return Product.objects.get(id=_id)

	def get_products_by_id(_id):
		return Product.objects.filter(id__in=_id)

	def get_product_by_title(_title):
		return Product.objects.get(title=_title)

	def search_product(_q):
		flag = ""

		for q in _q:
			if Product.objects.filter(title__icontains=q):
				flag = q		

		if flag == "":
			return flag
		else:
			return Product.objects.filter(title__icontains=flag)

	def __str__(self):
		return self.title

class Customer(models.Model):
	id = models.AutoField(primary_key=True)
	username = models.CharField(max_length=24, unique=True)
	password = models.CharField(max_length=24)
	first_name = models.CharField(max_length=16)
	last_name = models.CharField(max_length=16)
	phno = models.CharField(max_length=10)
	address = models.TextField(null=False)
	wishlist = models.CharField(max_length=200, default="{}")

	def get_customer_by_id(_id):
		return Customer.objects.get(id=_id)

	def get_customer_by_username(_uname):
		return Customer.objects.get(username=_uname)

	def __str__(self):
		return self.username

class Order(models.Model):
	STATUS = [
		("Pending", "PENDING"),
		("Shipped", "SHIPPED"),
		("Delivered", "DELIVERED"),
		("Canceled", "CANCELED"),
	]
	id = models.AutoField(primary_key=True)
	username = models.CharField(max_length=24)
	first_name = models.CharField(max_length=16)
	last_name = models.CharField(max_length=16)
	phno = models.CharField(max_length=10)
	email = models.CharField(max_length=24)
	address = models.TextField(null=False)
	amount = models.FloatField()
	duration = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=50, choices=STATUS, default=STATUS[0][0])

	def get_order_by_id(_id):
		return Order.objects.get(id=_id)

	def get_orders_by_username(_uname):
		return Order.objects.filter(username=_uname)
