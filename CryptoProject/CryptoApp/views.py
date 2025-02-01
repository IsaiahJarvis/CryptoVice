from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.apps import apps
from .models import Coin, User_Coin
from .scripts.submit_coin import run
import json
# Create your views here.
def marketcaptool(request):
    items = Coin.objects.all().order_by('-market_cap')
    return render(request, "marketcaptool.html", {"coins": items})

def user_submission(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        contract = data.get('contract')
        network = data.get('network')

        if check_for_dupes(contract) == False:
            network_names = {'Solana': '1399811149', 'Base': '8453', 'Arbitrum': '42161'}
            if network not in network_names:
                return JsonResponse({'message': f'{network} is not a supported network'})
            run(contract, network_names[network])
            return JsonResponse({'message': f'you entered: {contract}, {network}'})
        else:
            return JsonResponse({'message': f'This coin already exists'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def check_for_dupes(contract):
   model1 = apps.get_model('CryptoApp', 'Coin')
   model2 = apps.get_model('CryptoApp', 'User_Coin')

   return model1.objects.using('default').filter(contract_address=contract).exists() or \
          model2.objects.using('default').filter(contract_address=contract).exists()
