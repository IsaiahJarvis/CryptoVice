import requests
import json

def getHolders(uniqueId):
    url = "https://graph.codex.io/graphql"

    headers = {
      "content_type":"application/json",
      "Authorization": "50dbc45a02b5c68321bf2af1c6adc7e5390b4a47"
    }
    # Token ID for the query
    token_id = uniqueId

    all_holders = []
    cursor = None  # Start with no cursor
    counter = 0
    count = 0

    total_holders = 0
    total_holders_over10 = 0
    total_holders_over50 = 0
    total_holders_over100 = 0
    total_holders_over500 = 0
    total_holders_over1000 = 0
    total_holders_over2500 = 0

    while True:
        # Define the GraphQL query with cursor pagination
        query = f"""
        query GetTokenHolders {{
          holders(input: {{ tokenId: "{token_id}", cursor: {json.dumps(cursor)} }}) {{
            items {{
              walletId
              tokenId
              balance
              shiftedBalance
            }}
            count
            cursor
            status
          }}
        }}
        """
        # Make the request
        response = requests.post(url, headers=headers, json={"query": query})
        data = response.json()
        
        # Extract holders
        holders_data = data["data"]["holders"]
        holders = holders_data["items"]
        count = holders_data["count"]
        if counter < 1:
            total_holders = holders_data["count"]    
        # Append to the list
        all_holders.extend(holders)
        counter += len(holders)
        
        # Check if there's a next page (cursor) or break the loop
        if counter % 5000 == 0:
            print(counter)
        if counter > count:
            break
        elif all_holders[-1]["shiftedBalance"] < 10:
            break
        cursor = holders_data["cursor"]

    for x in all_holders:
        balance = float(x["shiftedBalance"])
        if balance > 250000:
            total_holders_over10 += 1
            total_holders_over50 += 1
            total_holders_over100 += 1
            total_holders_over500 += 1
            total_holders_over1000 += 1
            total_holders_over2500 += 1
        elif balance > 1000:
            total_holders_over10 += 1
            total_holders_over50 += 1
            total_holders_over100 += 1
            total_holders_over500 += 1
            total_holders_over1000 += 1
        elif balance > 500:
            total_holders_over10 += 1
            total_holders_over50 += 1
            total_holders_over100 += 1
            total_holders_over500 += 1
        elif balance > 100:
            total_holders_over10 += 1
            total_holders_over50 += 1
            total_holders_over100 += 1
        elif balance > 50:
            total_holders_over10 += 1
            total_holders_over50 += 1
        elif balance > 10:
            total_holders_over10 += 1
    holder_data = [total_holders,
                   total_holders_over10,
                   total_holders_over50,
                   total_holders_over100,
                   total_holders_over500,
                   total_holders_over1000,
                   total_holders_over2500]
    return holder_data

def run(uniqueId):
    return getHolders(uniqueId)

