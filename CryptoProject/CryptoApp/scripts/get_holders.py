import requests
import json

def getHolders(uniqueId):
    # Define the GraphQL query with cursor pagination
    url = "https://graph.codex.io/graphql"

    headers = {
      "content_type":"application/json",
      "Authorization": "50dbc45a02b5c68321bf2af1c6adc7e5390b4a47"
    }

    # Token ID for the query
    token_id = uniqueId

    all_holders = []
    cursor = None  # Start with no cursor

    query = f"""
    query GetTokenHolders {{
      holders(input: {{ tokenId: "{token_id}", cursor: {json.dumps(cursor)} }}) {{
        count
        top10HoldersPercent
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
    return holders_data["count"]

def run(uniqueId):
    return getHolders(uniqueId)
