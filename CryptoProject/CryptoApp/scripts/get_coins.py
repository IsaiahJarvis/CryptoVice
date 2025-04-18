from CryptoApp.models import Coin
from django.conf import settings
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

def call_cg_api():
    page = 1
    all_coins_data = []
    cg_key = settings.API_KEYS.get('coingecko_api')

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
                            store_wanted_data.append({'contract_address': "coingecko",
                                                      'crypto_id': x['id'],
                                                      'name': x['name'],
                                                      'symbol': x['symbol'],
                                                      'image_link': x['image'],
                                                      'market_cap': x['market_cap'],
                                                      'fdv': x['fully_diluted_valuation'],
                                                      'circ_supply': x['circulating_supply'],
                                                      'price': x['current_price'],
                                                      'network': "temp"})
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
    network_names = {'1399811149': 'Solana', '8453': 'Base', '42161': 'Arbitrum'}
    url = "https://graph.codex.io/graphql"
    codex_key = settings.API_KEYS.get('codex_api')

    headers = {
        "Content-Type": "application/json",
        "Authorization": codex_key
    }

    query = """
    query GetMarketCap($limit: Int, $offset: Int, $filters: TokenFilters) {
      filterTokens(limit: $limit, offset: $offset, filters: $filters) {
        count
        page
        results {
          token {
            address
            id
            name
            symbol
            networkId
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
        "marketCap": {"gt": 20000, "lt": 15000000000},  # Only include tokens where marketCap > 0
        "liquidity": {"gt": 20000},
        "holders": {"gt": 0},
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
        if token.get("token", {}).get("address", "N/A") == "AF3g85eVMgLt4KiANZu66cT24v94Za1RJQWGg6Vbpump":
            print("found")
        counter += 1
        fdv = float(token.get("marketCap", "N/A"))
        price = float(token.get("priceUSD", "N/A"))
        circulatingSupply = token.get("token", {}).get("info", {}).get("circulatingSupply", "N/A")
        market_cap = price * float(circulatingSupply)
        final_list.append({'contract_address': token.get("token", {}).get('address', "N/A"),
                           'crypto_id': token.get("token", {}).get("id", "N/A"),
                           'name': token.get("token", {}).get("name", "N/A"),
                           'symbol': token.get("token", {}).get("symbol", "N/A"),
                           'image_link': token.get("token", {}).get("info", {}).get("imageThumbUrl", "N/A"),
                           'market_cap': market_cap,
                           'fdv': fdv,
                           'circ_supply': circulatingSupply,
                           'price': price,
                           'network': str(token.get("token", {}).get("networkId", "N/A"))})
    print("BREAK")
    print(counter)
    return final_list

def call_codex_api():
    tokens = []
    networks = [1399811149, 42161, 8453]
    for x in networks:
        tokens.extend(get_tokens_codex(x))
    return tokens

def run():
    coin_data = call_codex_api()
    #coin_data.extend(call_cg_api())
    address_list = []
    
    if coin_data:
        Coin.objects.all().delete()
        for item in coin_data:
            cat_name = item['name'].replace("\x00", "")
            cat_id = item['crypto_id'].replace("\x00", "")
            cat_symbol = item['symbol'].replace("\x00", "")
            cat_image_link = item['image_link']
            cat_market_cap = item['market_cap']
            cat_FDV = item['fdv']
            cat_circ_supp = item['circ_supply']
            cat_price = item['price']
            cat_address = item['contract_address']
            cat_networkId = item['network']

            mixed_list = [cat_name, cat_id, cat_symbol, cat_image_link, cat_market_cap, cat_FDV, cat_circ_supp, cat_price, cat_address, cat_networkId]
            for item in mixed_list:
                if isinstance(item, str) and "\x00" in item:
                    print(mixed_list)
                    item = item.replace("\x00", "")

            if cat_address not in address_list and cat_address != "coingecko":
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
                address_list.append(cat_address)
            elif cat_address == "coingecko":
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
        print('Done')
        return True
    return False
    print('Failed')
