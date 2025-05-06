from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.apps import apps
from .models import Coin
from .tasks import getInfo
from celery.result import AsyncResult
import json
# Create your views here.
def marketcaptool(request):
    items = Coin.objects.all().order_by('-market_cap')
    return render(request, "marketcaptool.html", {"coins": items})

def image_page(request):
    return render(request, "tooltippage.html")

def get_info_filter(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            input_string = data.get("uniqueId", "")
            result_task = getInfo.apply_async(args=[input_string])
            return JsonResponse({"message": "Task started", "task_id": result_task.id})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)

def check_task_status(request, task_id):
    task = AsyncResult(task_id)
    if task.ready():
        result_dict = task.info or {}

        if not isinstance(result_dict, dict):
            return JsonResponse({"status": "FAILURE", "error": "No Data", "input_string": None, "data": None})

        input_string = result_dict.get("input_string")
        result_data = result_dict.get("data")
        if result_data:
            return JsonResponse({"status": "SUCCESS", "result": result_data})
        else:
            print("TASK", task_id, "FAILED")
            return JsonResponse({"status": "FAILURE", "error": "No Results"}, status=400)
    else:
        return JsonResponse({"task_id": task_id, "status": task.status, "result": None})

