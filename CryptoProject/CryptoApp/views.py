from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.apps import apps
from .models import Coin
from .scripts import get_holders, get_holders_with_filters
import json
# Create your views here.
def marketcaptool(request):
    items = Coin.objects.all().order_by('-market_cap')
    return render(request, "marketcaptool.html", {"coins": items})

def get_holders_quick(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            input_string = data.get("uniqueId", "")
            result = get_holders.run(input_string)
            return JsonResponse({"result": result})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)

def get_holders_filter(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            input_string = data.get("uniqueId", "")
            result = get_holders_with_filters.run(input_string)
            return JsonResponse({"result": result})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)


"""
def show_holders():
"""
