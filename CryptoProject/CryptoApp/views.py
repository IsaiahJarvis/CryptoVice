from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.apps import apps
from .models import Coin, HolderData
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
            if HolderData.objects.filter(unique_id=input_string).exists():
                matches = HolderData.objects.filter(unique_id=input_string)
                FIELDS_TO_RETRIEVE = ['total_holders', 'holders_over_10', 'holders_over_50', 
                                      'holders_over_100', 'holders_over_500', 'holders_over_1000', 
                                      'holders_over_2500']
                values_tuples = matches.values_list(*FIELDS_TO_RETRIEVE)
                result_array = [list(item) for item in values_tuples]
                result = result_array[0]
                return JsonResponse({"result": result})
            else:
                result = get_holders_with_filters.run(input_string)
                if (result):
                    save_holders(result, input_string)
                    return JsonResponse({"result": result})
                else:
                    return JsonResponse({"error": "No Results"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)


def save_holders(results, uniqueId):
    if results and len(results) >= 7:
        c = HolderData(unique_id = uniqueId,
                       total_holders = results[0],
                       holders_over_10 = results[1],
                       holders_over_50 = results[2],
                       holders_over_100 = results[3],
                       holders_over_500 = results[4],
                       holders_over_1000 = results[5],
                       holders_over_2500 = results[6])
        c.save()
