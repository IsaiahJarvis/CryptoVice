from django.shortcuts import render, HttpResponse
from .models import Coin

# Create your views here.
def marketcaptool(request):
    items = Coin.objects.all().order_by('-market_cap')
    return render(request, "marketcaptool.html", {"coins": items})

def submitcoin(request):
    return render(request, "submitcoin.html")
