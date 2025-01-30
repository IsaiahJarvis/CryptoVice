from django.contrib import admin
from .models import User_Coin, Coin

# Register your models here.
admin.site.register(Coin)
admin.site.register(User_Coin)

