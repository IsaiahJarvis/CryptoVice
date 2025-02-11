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
    #unique_id = models.CharField(max_length=255, unique=True)

#class TrackedCoin(models.Model):
#    unique_id = models.CharField(max_length=255, unique=True)
#    added_on = models.DateTimeField(auto_now_add=True)

#class HolderData(models.Model):
#    coin = models.ForeignKey(TrackedCoin, on_delete=models.CASCADE, related_name="holder_Data")
#    timestamp = models.DateTimeField(auto_now_add=True)
#    total_holders = models.IntegerField()
#    holders_over_10 = models.IntegerField()
#    holders_over_50 = models.IntegerField()
#    holders_over_100 = models.IntegerField()
#    holders_over_500 = models.IntegerField()
#    holders_over_1000 = models.IntegerField()
#    holders_over_2500 = models.IntegerField()
#    
#    class Meta:
#        ordering = ["-timestamp"]
