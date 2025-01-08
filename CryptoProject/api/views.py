from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from CryptoApp.models import Coin
from .serializers import CoinSerializer

class CoinPagination(PageNumberPagination):
    page_size = 50

@api_view(['GET'])
def searchCoins(request):
    query = request.GET.get('q', '')
    paginator = CoinPagination()
    if query:
        coins = Coin.objects.filter(Q(name__icontains=query) | Q(contract_address__icontains=query)).order_by('-market_cap')
        results = paginator.paginate_queryset(coins, request)
        serializer = CoinSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)
    else:
        coins = Coin.objects.all().order_by('-market_cap')
        results = paginator.paginate_queryset(coins, request)
        serializer = CoinSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)
