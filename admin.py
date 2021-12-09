from django.contrib import admin
from .models import *
admin.site.register(Person)
admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(ShowItem)
admin.site.register(BuyItem)
admin.site.register(AddMoney)

