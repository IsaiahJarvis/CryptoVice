from rest_framework import serializers
from CryptoApp.models import Coin

class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = '__all__'
