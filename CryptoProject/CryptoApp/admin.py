from django.contrib import admin
from .models import Coin, HolderData

# Register your models here.
admin.site.register(Coin)
admin.site.register(HolderData)
