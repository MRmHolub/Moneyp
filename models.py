from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser
from datetime import datetime


# Create your models here.
class Person(AbstractBaseUser):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
	username = models.CharField(max_length=200, unique=True) 
	email=models.CharField(max_length = 200) #odkazuje na páníčka z třáídy Person, 
	is_active = models.BooleanField(default=False) 
	creation_time =models.DateTimeField(auto_now_add=True, null=True) 
	USERNAME_FIELD ='username' 
	REQUIRED_FIELDS = ["username,email,password"]

	def __str__(self): return f"\nUsername: {self.username}\n"

	def __repr__(self): return f"\nUsername: {self.username}\nEmail:{self.email}\nCreated: {self.creation_time}\n"

class Customer(models.Model):
	person = models.OneToOneField(Person, on_delete=models.CASCADE, default=None)
	money_spend = models.IntegerField(default=0)
	bills = models.TextField(default="")


	def spend(self,carts):
		return sum(c.prize for c in carts)

	def __repr__(self):
		return f"\nCustomer: {self.person.username}\nSpend: {self.money_spend}\n"

	def __str__(self):
		return f"{self.person.username}"

class Cart(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	prize = models.IntegerField(default=0)
	date = models.CharField(max_length=200, default="01.01.2000")
	item_amount = models.IntegerField(default=1)
	place = models.CharField(max_length=255)
	cart = models.TextField(default="")
	compare_date = models.CharField(null=True,max_length=8)

	class Meta:
		ordering = ("compare_date",)#to make a reverse use - in front of

	def __str__(self):
		return f"{self.place}, {self.prize}"

	def __repr__(self):
		return f"\nPlace: {self.place}\nPrize: {self.prize}\nDate: {self.date}\nAmount of Items: {self.item_amount}\n"	

	def save(self, *args, **kwargs):
	    if not self.compare_date:
	        self.compare_date = str(self.date[6:10])+str(self.date[3:5])+str(self.date[0:2])
	    super(Cart, self).save(*args, **kwargs)

	def json_serialize(self):
		return {"id":self.id,
		"prize":self.prize,
		"date":self.date,
		"compare_date":self.compare_date,#x["date"][3:5] or x["date"][0:2] or x["date"][5:7]))
		"day":self.date[:2],
		"month":self.date[:5],
		"item_amount":self.item_amount,
		"place":self.place}


class ShowItem(models.Model):
	title = models.CharField(max_length=255)
	client = models.CharField(max_length=100)
	section = models.CharField(max_length=100)

	def __str__(self):
		return f"{self.title}"

	def __repr__(self):
		return f"This is {self.title}\nbought for your {self.client}"

class AddMoney(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=None)
	sponsor = models.CharField(max_length=200, default="Parents")
	amount = models.IntegerField(default=0)
	date = models.CharField(max_length=200, default="01.01.2000")

	def __str__(self):
		return f"{self.sponsor} {self.amount}"

	def __repr__(self):
		return f"{self.amount} From {self.sponsor} at {self.date}"

	def json_serialize(self):
		return {"id":self.id,
		"sponsor":self.sponsor,
		"amount":self.amount,
		"date":self.date}

class BuyItem(models.Model):
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE, default=None, null=True)
	prize = models.IntegerField(default=0)
	amount = models.IntegerField(default=1)
	weight = models.CharField(max_length=100,default=1,blank=True)
	title = models.CharField(max_length=255)
	info = models.TextField(default="",blank=True)
	client = models.CharField(max_length=100)
	section = models.CharField(max_length=200)
	thing = models.CharField(max_length=200,blank=True)

	def json_serialize(self):
		return {"id":self.id,
		"prize":self.prize,
		"amount":self.amount,
		"weight":self.weight,
		"title":self.title,
		"info":self.info,
		"client":self.client,
		"section":self.section,
		"thing":self.thing
		}
	def __str__(self):
		return f"{self.title}"

	def __repr__(self):
		return f"\nItem: {self.title}\nAmount: {self.amount}\nBought for:{self.client}\nTotal cost: {self.amount*self.prize}\r\n"


		