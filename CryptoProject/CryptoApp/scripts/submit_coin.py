from django.conf import settings
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

def get_token(contract_address, networkId):
    network_names = {'1399811149': 'Solana', '8453': 'Base', '42161': 'Arbitrum'}
    codex_key = settings.API_KEYS.get('codex_api')
    url = "https://graph.codex.io/graphql"
    token = str(contract_address) + ":" + str(networkId)
    headers = {
        "Content-Type": "application/json",
        "Authorization": codex_key
    }

    query = """
    query GetMarketCap($limit: Int, $offset: Int, $filters: TokenFilters, $tokens: [String]) {
      filterTokens(limit: $limit, offset: $offset, filters: $filters, tokens: $tokens) {
        count
        page
        results {
          token {
            name
            address
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

    limit = 1
    offset = 0
    
    # Define the filter to exclude tokens with no marketCap
    filters = {
    }
    
    try:
        response = requests.post(
            url,
            headers=headers,
            json={"query": query, "variables": {"limit": limit, "offset": offset, "filters": filters, "tokens": [token]}}
        )

        if response.status_code != 200:
            print(f"HTTP Error {response.status_code}: {response.text}")

        data = response.json()
        #print("Raw Response:", json.dumps(data, indent=2))  # Debugging

        # Check if "data" exists
        if "data" not in data or "filterTokens" not in data["data"]:
            print("Error in response:", data)

        token = data["data"]["filterTokens"]["results"]
        token = token[0]
        
        fdv = float(token.get("marketCap", "N/A"))
        price = float(token.get("priceUSD", "N/A"))
        circulatingSupply = token.get("token", {}).get("info", {}).get("circulatingSupply", "N/A")
        market_cap = price * float(circulatingSupply)
        token_input = {'contract_address': token.get("token", {}).get('address', "N/A"),
                       'crypto_id': token.get("token", {}).get("id", "N/A"),
                       'name': token.get("token", {}).get("name", "N/A"),
                       'symbol': token.get("token", {}).get("symbol", "N/A"),
                       'image_link': token.get("token", {}).get("info", {}).get("imageThumbUrl", "N/A"),
                       'market_cap': market_cap,
                       'fdv': fdv,
                       'circ_supply': circulatingSupply,
                       'price': price,
                       'network': network_names[str(token.get("token", {}).get("networkId", "N/A"))]}
        return token_input
    except Exception as e:
        print(f"An error occurred: {e}")

def run(contract_address, networkId):
    coin_data = get_token(contract_address, networkId)
    print(coin_data)
    try:
        cat_name = coin_data['name']
        cat_id = coin_data.get('crypto_id', 'Unknown ID')
        cat_symbol = coin_data.get('symbol', 'Unknown Symbol')
        cat_image_link = coin_data['image_link']
        cat_market_cap = coin_data['market_cap']
        cat_FDV = coin_data['fdv']
        cat_circ_supp = coin_data['circ_supply']
        cat_price = coin_data['price']
        cat_address = coin_data['contract_address']
        cat_networkId = coin_data['network']

        c = User_Coin(name = cat_name,
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
    except Exception as e:
        print(f"Error saving to database: {e}")
