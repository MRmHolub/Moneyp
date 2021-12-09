from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib import messages
from .mail_validate import *
from .models import *
from datetime import datetime




def loginPage(response):
	"""This function renders input fields, if loged for a first time it creates a Customer object from the Person obejct and put the Customer object in a session,
	else find a customer in database (by the id of person whom it loged for and puts its customer object to session, redirects to home page"""
	if response.method == "POST":
		print("POST RESPONSE IN LOGIN: ",response.POST)
		form = LoginPerson(response.POST)

		try: 

			password = response.POST["password"]
			username = response.POST["username"]
			print(password,username)
			user = authenticate(response, username=username, password=password) #když použiji get, tak pokud dané jméno neexistuje vyhodí mi to error, pokud bych použil filter, tak mi to vyhodí prázdný query set
			print(user)
			if (user is not None) or (response.session["loged"]==True):
				response.session["loged"]=True
				login(response,user)
				person = Person.objects.get(username=username)
				try:
					customer = Customer.objects.get(id=person.id)
					response.session["customer"]=customer.id
					return redirect("home")
				except:
					customer = Customer.objects.create(person=person)
					customer.save()
					response.session["customer"]=customer.id
					return redirect("home")
		except:
			response.session["loged"]=False
			messages.error(response, "Wrong username or password, try again")
	else:
		form = LoginPerson()

	context={"form":form}
	return render(response, "main/login.html", context)

def sign(response):
	"""Function for creating a new account,sends special confirmation code to your email to check mail validation"""
	if response.method == "POST":
		form = CreateNewPerson(response.POST)
		print(response.POST)
		try:
			form.is_valid()
			username, email = response.POST.get("username"),response.POST.get("email")
			auth_code=my_auth(username,email) #authorizacni fce
			print("Email code: ",auth_code)
			response.session["auth_code"]=auth_code
			response.session["resp_POST"]=response.POST
		
			return redirect("welcome") #redirectuje na fci v tomto skriptu
		except:
			print("zas je něco zle",response.POST,form.errors)	
	else:
		form = CreateNewPerson() 


	context = {"form":form}
	return render(response, "main/sign_up.html", context)

def welcome(response):
	"""Function taking care of special codes from newcomers for email validation"""

	if response.method == "POST":
		print("POST RESPONSE IN WELCOME Func: ",response.POST)
		form=CheckNewPerson(response.POST)
		if response.POST.get("validate") == response.session["auth_code"]:
			create_new_user(response)
			return redirect('login')
		elif response.POST.get("validate") == response.session["change_mail_code"]:
			customer = Customer.objects.get(id=response.session["customer"])
			customer.person.email = response.session["change_mail_code"]
			customer.person.save()
			del response.session["change_mail_code"]
			return redirect("home")

		else:
			return redirect("fail_email_validation")
	else:
		form = CheckNewPerson()
	context = {"form":form}
	return render(response, "main/welcome_new_user.html", context)

def fail_email_validation(response):
	"""Function that renders page for another tries in putting up special codes from mail"""
	if response.method == "POST":
		form=CheckNewPerson(response.POST)
		if response.POST.get("validate") == response.session["auth_code"]:
			create_new_user(response)
			return redirect("login")
		else:
			messages.error(response, "Wrong Code, try again!")
	else:
		form = CheckNewPerson()
	context = {"form":form}
	return render(response, "main/fail_email_validation.html",context)
	
def create_new_user(response):
	del response.session["auth_code"]
	#saving a person to do Person data and deleting its properties from cookie
	print("Ucet byl potvrzen, zakladam ho")
	messages.success(response,"Your account was created!")
	form = CreateNewPerson(response.session["resp_POST"])
	try:
		form.is_valid()
		form.save()
	except:
		print(form.errors)

		
	del response.session["resp_POST"]
	#adding a person object to cookie and creating a customer from this person and adding him to cookie
	print(form.cleaned_data.get("username"),"Ussr is: ",response.user)
	user=User.objects.get(username=form.cleaned_data.get("username") )
	person = Person(user=user, email=user.email, username = user.username)
	person.save()
	customer = Customer.objects.create(person=person)
	customer.save()
	response.session["customer"]=customer.id

def logoutPage(response):
	response.session["loged"]=False
	print("Logging out, the sessions: ",response.session.items())
	logout(response)
	return redirect("login")
