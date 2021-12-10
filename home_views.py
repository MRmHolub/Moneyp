from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import *
from django.contrib import messages
from .models import *
from datetime import datetime
from .mail_validate import *
from django.contrib.auth import authenticate


def loged_decorator(func):
	"""Decorator function making sure customer is loged so someone doesn't access the site without making na account, prevent crashes from request from non existing user"""
	def deco_wrapper(response,*args,**kwargs):
		try:
			print("Sessions :",response.session.items(),args,kwargs)
			response.session["loged"] == True
			return func(response,*args,**kwargs)
		except:
			return redirect("login")
	return deco_wrapper

@loged_decorator
def home(response):
	response.session["cart"]=[]
	response.session["prize"]=0
	response.session["amount"]=0
	print("Session items: ",response.session.items())
	return render(response, "main/home.html",{})
	

#@loged_decorator
def settings(response):

	customer=Customer.objects.get(id=response.session["customer"])
	if response.method=="POST":
		print("SETTINGS",response.POST)

		if response.session["change_pass"]:
			pass1=response.POST["password1"]
			pass2=response.POST["password2"]
			if pass1 == pass2:
				response.user.set_password(pass1)
				response.user.save()
				print(response.user.password)
				messages.success(response,"Your password was successfully changed")
				print("Heslo bylo zmeneno na: ",pass1)
				#posilam mail o zmene jmena
				response.session["change_pass"]=False
				return redirect("settings")
			else:
				messages.error(response,"These two passwords didn't match!")	

		else:
			password=response.POST["password"]
			username = response.POST["username"]
			email = response.POST["email"]
			curr_email = customer.person.email
			print("Current mail",curr_email,"New mail",email,"Name",username)

			if username!=customer.person.username:
				new_username(curr_email,customer.person.username, username)
				customer.person.username = username
				customer.person.save()
				messages.success(response,"Your name was successfully changed")
			else:
				user = authenticate(response, username=username, password=password)
				if user is not None:
					if response.POST.get("change_pass",False):
						print("Heslo je spravne oteviram formu pro nove heslo")
						response.session["change_pass"]=True
					elif email!=curr_email:
						messages.warning(response,"To change email you need to confirm it first.")
						sk = new_mail(curr_email,customer.person.username)
						response.session["change_mail_code"]=sk
						return redirect("welcome_new_user")
				else:
					messages.error(response,"You need to fill correct password!")
	else:
		form = NewSettings()
		response.session["change_pass"]=False

	context={"customer":customer, "change_pass":response.session["change_pass"]}
	return render(response, "main/settings.html", context)

@loged_decorator
def flat(response):
	if response.method == "POST":
		print("POST RESPONSE IN FLAT: ",response.POST)
		return post_handler(response)
	else:
		form=NewCartItem()


	hygiene = section_filter(client="flat", section="Hygiene")
	kitchen = section_filter(client="flat", section="Kitchen")
	garden = section_filter(client="flat", section="Garden")
	plants = section_filter(client="flat", section="Plants")
	items = {"Hygiene": hygiene,"Kitchen":kitchen,"Garden":garden, "Plants":plants}
	#print(list([k,v] for k,v in items.items()))
	content = {"items":items, "form":form}
	return render(response, "main/flat.html",content)

@loged_decorator
def school(response):
	if response.method == "POST":
		print("POST RESPONSE IN SCHOOL: ",response.POST)
		return post_handler(response)
	else:
		form=NewCartItem()


	books = section_filter(client="school", section="Books")
	rest = section_filter(client="school", section="Rest")
	items = {"Books":books, "Rest":rest}
	#print(list([k,v] for k,v in items.items()))
	content = {"items":items, "form":form}
	return render(response, "main/school.html",content)

@loged_decorator
def others(response):
	if response.method == "POST":
		print("POST RESPONSE IN OTHERS: ",response.POST)
		return post_handler(response)
	else:
		form=NewCartItem()

	rest = section_filter(client="others", section="Rest")
	travel = section_filter(client="others", section="Travel")
	sports = section_filter(client="others", section="Sports")
	clothes = section_filter(client="others", section="Clothes")
	charity = section_filter(client="others", section="Charity")
	items = {"Travel":travel, "Sports":sports,"Rest":rest, "Clothes":clothes, "Charity":charity}
	content = {"items":items, "form":form}
	return render(response, "main/others.html",content)

@loged_decorator
def food(response):
	if response.method == "POST":
		print("POST RESPONSE IN FOOD: ",response.POST)
		return post_handler(response)
	else:
		form=NewCartItem()

	butchery = section_filter(client="food", section="Butchery")
	bakery = section_filter(client="food", section="Bakery")
	plants = section_filter(client="food", section="Fruits & Vegetables")
	cooking_ingredients = section_filter(client="food", section="Cooking Ingredients")
	snacks = section_filter(client="food", section="Snacks")
	drinks = section_filter(client="food", section="Drinks")
	side_dishes = section_filter(client="food", section="Side Dishes")
	fast_foods = section_filter(client="food", section="Fast Food")
	milk_products = section_filter(client="food", section="Milk products")
	items = {"Butchery":butchery, "Bakery":bakery, "Fruits & Vegetables":plants, "Cooking Ingredients":cooking_ingredients, "Snacks":snacks, "Drinks": drinks, "Side Dishes":side_dishes, "Fast Food":fast_foods, "Milk products": milk_products}
	#print(list([k,v] for k,v in items.items()))
	
	content = {"items":items, "form":form}
	return render(response, "main/food.html",content)

def section_filter(client, section):
	items = filter(lambda x: x.client==client, ShowItem.objects.all()) #vyfiltruju itemy(school,flat...)
	return list(filter(lambda y: y.section==section,items))#vyfiltruju itemy podle sekce

def finish_form(response,form):
	try:
		form.is_valid()
		x = form.save()
		return x
	except:
		print(response,form)
		print(form.errors)
		messages.error(response, "You need to fill all fields correctly to add new item!")

def post_handler(response):
	customer = Customer.objects.get(id=response.session["customer"])

	if response.POST.get("new_show_item"): #prvně potřeba udělat input formu v html template pro tuto fci a nasledne pridat button s touto hodnotou
		if not ShowItem.objects.filter(title=response.POST.get("title")):
			form = NewShowItem(response.POST)
			finish_form(response,form)
		return redirect(response.POST.get("client"))

	elif response.POST.get("end"):
		items = "\n".join(str(res) for res in response.session["cart"])
		print("Items in cart, put in Cart object",items)
		prize = response.session["prize"]
		amount = response.session["amount"]
		form = Cart(customer=customer, cart=items, prize=prize ,place=response.POST.get("place"),
					 item_amount=amount, date=datetime.now().strftime("%d.%m.%Y"))
		form.save()
		carts = Cart.objects.filter(customer=customer)
		customer.bills += repr(form)
		customer.money_spend = customer.spend(carts=carts)
		customer.save()
		non_cart_items = BuyItem.objects.filter(cart=None)
		
		for cart in carts:
			tmp_cartcart = cart.cart.split("[{'id': ")[1:]
			for tmp_id in tmp_cartcart:
				the_id = int(tmp_id[0:3].replace(",","").replace(" ",""))
				for item in non_cart_items:
					print("ID of BuyItem missing cart",tmp_id)
					if item.id == the_id:
						item.cart = cart
						item.save()
		
		BuyItem.objects.filter(cart=None).delete()

		del response.session["cart"]
		del response.session["amount"]
		del response.session["prize"]
		print("Deleted cart session items")
		return redirect("home")

	elif response.POST.get("add_to_cart"):
		form = NewCartItem(response.POST)
		cart_item = finish_form(response,form)
		print("Form for adding ot cart and POST response",form.cleaned_data.items(), response.POST)
		q_set = BuyItem.objects.filter(id=cart_item.id) #filter vrati query set, get vrati objekt
		obj = BuyItem.objects.get(id=cart_item.id) #filter vrati query set, get vrati objekt
		data = [data.json_serialize() for data in q_set]
		print("DATA",data)
		response.session["cart"]+=data
		response.session["prize"]+=int(obj.amount * obj.prize)
		response.session["amount"]+=int(obj.amount)
		print("Added to this cart",response.session["cart"])
		return redirect(response.POST.get("client"))

	elif response.POST.get("delete_thing"):
		item_to_del = "".join(response.POST.get("delete_thing").split("_")[1:])
		print("Item to del",item_to_del)
		ShowItem.objects.filter(title=item_to_del).delete()
		return redirect(response.POST.get("client"))