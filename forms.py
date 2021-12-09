from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm #vytvoří formu zadaného modelu, 
from .models import *
from django.contrib.auth.models import User


class CreateNewPerson(UserCreationForm):
	class Meta:
		model = User
		fields = ["username", "email","password1","password2"]

class CheckNewPerson(forms.Form):
	validate = forms.CharField(max_length=150)

class LoginPerson(ModelForm):
	class Meta:
		model = Person
		fields = ["username","password"]

class NewCartItem(ModelForm):
	class Meta:
		model = BuyItem
		fields = ["title","prize","amount","weight","info","client","section","thing"]

class NewShowItem(ModelForm):
	class Meta:
		model = ShowItem
		fields = ["title", "client","section"]

class NewSettings(ModelForm):
	class Meta:
		model=Person
		fields=["username","email","password"]