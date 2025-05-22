from CryptoApp.models import Coin
from django.conf import settings
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

API_URL = "http://45.141.233.150:8000/data"

def main():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Raises HTTPError if the request returned an unsuccessful status code
        data = response.json()
        print("Response from the API:")
        store(data["results"])
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

def store(data):
    if data:
        Coin.objects.all().delete()
        for item in data:
            cat_name = item['name']
            cat_id = item['crypto_id']
            cat_symbol = item['symbol']
            cat_image_link = item['image']
            cat_market_cap = item['market_cap']
            cat_FDV = item['fdv']
            cat_circ_supp = item['circ_supply']
            cat_price = item['price']
            cat_address = item['address']
            cat_networkId = item['network']
            
            c = Coin(name = cat_name,
                     crypto_id = cat_id,
                     symbol = cat_symbol,
                     image_link = cat_image_link,
                     market_cap = cat_market_cap,
                     fdv = cat_FDV,
                     circulating_supply = cat_circ_supp,
                     price = cat_price,
                     contract_address = cat_address,
                     network = cat_networkId)
            c.save()


if __name__ == "__main__":
    main()
