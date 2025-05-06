from CryptoApp.scripts.get_coins import run
from CryptoApp.scripts.calculate_metrics import calculate_metrics
from celery import group, shared_task, current_task
from celery.exceptions import SoftTimeLimitExceeded
from datetime import datetime
import logging
from collections import defaultdict
from django.conf import settings
from celery.utils.log import get_task_logger
from django.utils.timezone import now
from datetime import timedelta
import requests
import json

logger = get_task_logger(__name__)

@shared_task(soft_time_limit=1200, time_limit=1500, queue='user_queue')
def getInfo(uniqueId):
    try:
        start_time = datetime.now()
        url = "https://graph.codex.io/graphql"

        codex_key = settings.API_KEYS.get('codex_api')

        headers = {
          "content_type":"application/json",
          "Authorization": codex_key
        }
        # Token ID for the query
        token_id = uniqueId

        all_holders = []
        cursor = None  # Start with no cursor
        counter = 0
        count = 0
        filters = {}
        

        query = """
        query GetMarketCap($limit: Int, $offset: Int, $filters: TokenFilters, $tokens: [String]) {
            filterTokens(limit: $limit, offset: $offset, filters: $filters, tokens: $tokens) {
                count
                page
                results {
                    buyCount1
                    buyCount4
                    buyCount5m
                    buyCount12
                    buyCount24
                    sellCount1
                    sellCount4
                    sellCount5m
                    sellCount12
                    sellCount24
                    volume1
                    volume4
                    volume5m
                    volume12
                    volume24
                    uniqueBuys1
                    uniqueBuys4
                    uniqueBuys5m
                    uniqueBuys12
                    uniqueBuys24
                    uniqueSells1
                    uniqueSells4
                    uniqueSells5m
                    uniqueSells12
                    uniqueSells24
                    txnCount1
                    txnCount4
                    txnCount5m
                    txnCount12
                    txnCount24
                    high1
                    high4
                    high5m
                    high12
                    high24
                    low1
                    low4
                    low5m
                    low12
                    low24
                    priceUSD
                    swapPct1dOldWallet
                }
            }
        }
        """

        limit = 50
        offset = 0
        tokens = [uniqueId]
        grouped_data = defaultdict(dict)

        try:
            response = requests.post(
                url,
                headers=headers,
                json={"query": query, "variables": {"limit": limit, "offset": offset, "filters": filters, "tokens": tokens}}
            )

            data = response.json()

            token_info = data.get("data", {}).get("filterTokens", {}).get("results", "N/A")
            print(token_info)
            
        except(requests.RequestException, ValueError, KeyError, IndexError) as e:
            print(f"Error fetching holders: {e}")
            return {"input_string": None, "data": None}

        for key, value in token_info[0].items():
            if key == "priceUSD" or key == "swapPct1dOldWallet":
                grouped_data[key] = value
            else:
                suffix_start = len(key.rstrip('0123456789m'))
                suffix = key[suffix_start:]
                metric_name = key[:suffix_start]
                new_key = f"filter{suffix}"
                grouped_data[new_key][metric_name] = value

        # Convert defaultdict to a regular dictionary for final output
        raw_output = dict(grouped_data)
        
        final_output = calculate_metrics(raw_output)
        # Example of accessing the data

        return {"input_string": uniqueId, "data": final_output}
    
    except SoftTimeLimitExceeded:
        current_task.update_state(state="FAILURE", meta={"error": "Soft timeout exceeded"})
        return {"status": "FAILURE", "error": "Soft timeout exceeded", "input_string": None, "data": None}

    except Exception as e:
        exc_type = type(e).__name__
        current_task.update_state(
            state="FAILURE",
            meta={"exc_type": exc_type, "exc_message": str(e)}
        )
        return {"status": "FAILURE", "error": str(e), "input_string": None, "data": None}

def update_coins():
    if run() == True:
        print('Database updated')
    else:
        print('Database not updated')
    
