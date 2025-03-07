from CryptoApp.scripts.get_coins import run
from celery import shared_task, current_task
from celery.exceptions import SoftTimeLimitExceeded
from datetime import datetime
import logging
from django.conf import settings
from celery.utils.log import get_task_logger
from django.utils.timezone import now
from datetime import timedelta
from .models import HolderData
import requests
import json

logger = get_task_logger(__name__)

# Create a handler for the systemd journal

@shared_task(queue='scheduled_queue')
def checkHolders():
    expiration_time = now() - timedelta(minutes=15)
    HolderData.objects.filter(timestamp__lt=expiration_time).delete()

#@shared_task(queue='holder_queue')
#def getHoldersScheduled(uniqueId):


@shared_task(soft_time_limit=1200, time_limit=1500, queue='user_queue')
def getHolders(uniqueId):
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

        total_holders = 0
        total_holders_over10 = 0
        total_holders_over50 = 0
        total_holders_over100 = 0
        total_holders_over500 = 0
        total_holders_over1000 = 0
        total_holders_over2500 = 0

        while True:
            if (datetime.now() - start_time).seconds > 1200:
                return {"input_string": None, "data": None}
            # Define the GraphQL query with cursor pagination
            query = f"""
            query GetTokenHolders {{
              holders(input: {{ tokenId: "{token_id}", cursor: {json.dumps(cursor)}, sort: { attribute: 'BALANCE', direction: 'DESC' } }}) {{
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

            try:
                # Make the request
                response = requests.post(url, headers=headers, json={"query": query})
                response.raise_for_status()
                data = response.json()
                
                if "data" not in data or "holders" not in data["data"]:
                    raise ValueError("Invalid API response structure")

                # Extract holders
                holders_data = data.get("data", {}).get("holders", "N/A")
                holders = holders_data.get("items", {})
                count = holders_data.get("count", 0)

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
            
            except(requests.RequestException, ValueError, KeyError, IndexError) as e:
                print(f"Error fetching holders: {e}")
                return {"input_string": None, "data": None}


        if not all_holders:
            return {"input_string": None, "data": None}

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
        return {"input_string": uniqueId, "data": holder_data}
    
    except SoftTimeLimitExceeded:
        current_task.update_state(state="FAILURE", meta={"error": "Soft timeout exceeded"})
        return {"status": "FAILURE", "error": "Soft timeout exceeded", "input_string": None, "data": None}

    except Exception as e:
        current_task.update_state(state="FAILURE", meta={"error": str(e)})
        return {"status": "FAILURE", "error": str(e), "input_string": None, "data": None}

def update_coins():
    if run() == True:
        print('Database updated')
    else:
        print('Database not updated')
    
