from CryptoApp.models import Coin
from django.conf import settings
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

def call_cg_api():
    page = 1
    all_coins_data = []
    cg_key = settings.API_KEYS.get('coingecko_api')
    codex_key = settings.API_KEYS.get('codex_api')

    while True:
        try:
            url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&per_page=250&page=" + str(page)
            headers = {
                "accept": "application/json",
                "x-cg-demo-api-key": cg_key,
            }

            response = requests.get(url, headers=headers)
            data = json.loads(response.text)
            store_wanted_data = []

            if data:
                for x in data:
                    if x['circulating_supply'] is not None and x['market_cap'] is not None:
                        if int(x['circulating_supply']) != 0 and int(x['market_cap']) != 0:
                            store_wanted_data.append({'crypto_id': x['id'], 'name': x['name'],'symbol': x['symbol'], 'image_link': x['image'], 'market_cap': x['market_cap'], 'fdv': x['fully_diluted_valuation'], 'circ_supply': x['circulating_supply'], 'price': x['current_price']})
            else:
                print("No data found in the response")
                break

            all_coins_data.extend(store_wanted_data)

            page += 1
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
            return None

    return all_coins_data

def get_tokens_codex(network):
    url = "https://graph.codex.io/graphql"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "9f436aa47fa4d649d9344893ad3ad8b1d71a92c9"
    }

    query = """
    query GetMarketCap($limit: Int, $offset: Int, $filters: TokenFilters) {
      filterTokens(limit: $limit, offset: $offset, filters: $filters) {
        count
        page
        results {
          token {
            id
            name
            symbol
            info {
              circulatingSupply
              imageThumbUrl
            }
          }
          marketCap
          priceUSD
          liquidity
        }
      }
    }
    """

    limit = 50
    offset = 0
    all_tokens = []

    # Define the filter to exclude tokens with no marketCap
    filters = {
        "marketCap": {"gt": 50000, "lt": 250000000},  # Only include tokens where marketCap > 0
        "liquidity": {"gt": 30000},
        "network": [network]
    }

    while True:
        try:
            response = requests.post(
                url,
                headers=headers,
                json={"query": query, "variables": {"limit": limit, "offset": offset, "filters": filters}}
            )

            if response.status_code != 200:
                print(f"HTTP Error {response.status_code}: {response.text}")
                break

            data = response.json()

            # Check if "data" exists
            if "data" not in data or "filterTokens" not in data["data"]:
                print("Error in response:", data)
                break

            tokens = data["data"]["filterTokens"]["results"]
            all_tokens.extend(tokens)

            # Check if we've reached the end of the list
            if len(tokens) < limit:
                break

            offset += limit  # Fetch the next page

        except Exception as e:
            print(f"An error occurred: {e}")
            break

    # Print fetched tokens
    counter = 0
    final_list = []
    for token in all_tokens:
        counter += 1
        fdv = float(token.get("marketCap", "N/A"))
        price = float(token.get("priceUSD", "N/A"))
        circulatingSupply = token.get("token", {}).get("info", {}).get("circulatingSupply", "N/A")
        market_cap = price * float(circulatingSupply)
        final_list.append({'crypto_id': token.get("token", {}).get("id", "N/A"),
                           'name': token.get("token", {}).get("name", "N/A"),
                           'symbol': token.get("token", {}).get("symbol", "N/A"),
                           'image_link': token.get("token", {}).get("info", {}).get("imageThumbUrl", "N/A"),
                           'market_cap': market_cap,
                           'fdv': fdv,
                           'circ_supply': circulatingSupply,
                           'price': price})
    print("BREAK")
    print(counter)
    return final_list

def call_codex_api():
    tokens = []
    networks = [1399811149, 42161]
    for x in networks:
        tokens.extend(get_tokens_codex(x))
    return tokens

def run():
    coin_data = call_cg_api()
    coin_data.extend(call_codex_api())
    
    if coin_data:
        Coin.objects.all().delete()
        for item in coin_data:
            cat_name = item['name']
            cat_id = item['crypto_id']
            cat_symbol = item['symbol']
            cat_image_link = item['image_link']
            cat_market_cap = item['market_cap']
            cat_FDV = item['fdv']
            cat_circ_supp = item['circ_supply']
            cat_price = item['price']

            c = Coin(name = cat_name, crypto_id = cat_id, symbol = cat_symbol, image_link = cat_image_link, market_cap = cat_market_cap, fdv = cat_FDV, circulating_supply = cat_circ_supp, price = cat_price)

            c.save()
        print('Done')
        return True
    return False
    print('Failed')
