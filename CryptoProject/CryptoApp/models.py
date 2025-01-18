from django.db import models

# Create your models here.

class Coin(models.Model):
    name = models.CharField(max_length=100)
    crypto_id = models.CharField(max_length=100)
    symbol = models.CharField(max_length=100)
    image_link = models.URLField(null=True, blank=True, max_length=2000)
    fdv = models.DecimalField(null=True, blank=True, max_digits=100, decimal_places=10)
    market_cap = models.DecimalField(null=True, blank=True, max_digits=100, decimal_places=10)
    circulating_supply = models.CharField(null=True, blank=True)
    price = models.DecimalField(null=True, blank=True, max_digits=100, decimal_places=10)
    contract_address = models.CharField(null=True, blank=True)
    network = models.CharField(null=True, blank=True)
