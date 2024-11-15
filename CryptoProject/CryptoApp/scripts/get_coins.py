from CryptoApp.models import Coin
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

def call_api():
    page = 1
    all_coins_data = []

    while True:
        try:
            url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&per_page=250&page=" + str(page)
            headers = {
                "accept": "application/json",
                "x-cg-demo-api-key": "CG-in2YGZGTF6muWi1GGjesxQ8p",
            }

            response = requests.get(url, headers=headers)
            data = json.loads(response.text)
            store_wanted_data = []

            if data:
                for x in data:
                    if x['circulating_supply'] is not None and x['market_cap'] is not None:
                        if int(x['circulating_supply']) != 0 and int(x['market_cap']) != 0:
                            store_wanted_data.append({'crypto_id': x['id'], 'name': x['name'],'symbol': x['symbol'], 'image_link': x['image'] , 'market_cap': x['market_cap'], 'circ_supply': x['circulating_supply'], 'price': x['current_price']})
            else:
                print("No data found in the response")
                break

            all_coins_data.extend(store_wanted_data)

            page += 1
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
            return None

    return all_coins_data

def run():
    coin_data = call_api()
    
    if coin_data:
        Coin.objects.all().delete()
        for item in coin_data:
            cat_name = item['name']
            cat_id = item['crypto_id']
            cat_symbol = item['symbol']
            cat_image_link = item['image_link']
            cat_market_cap = item['market_cap']
            cat_circ_supp = item['circ_supply']
            cat_price = item['price']

            c = Coin(name = cat_name, crypto_id = cat_id, symbol = cat_symbol, image_link = cat_image_link, market_cap = cat_market_cap, circulating_supply = cat_circ_supp, price = cat_price)

            c.save()
        print('done')
