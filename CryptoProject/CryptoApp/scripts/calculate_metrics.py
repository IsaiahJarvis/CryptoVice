def calculate_metrics(entry):

    final = {}

    for x in entry:
        if x != "priceUSD" and x != "swapPct1dOldWallet" and x != "isScam":
            try:
                high = float(entry[x]["high"])
                low = float(entry[x]["low"])
            except (TypeError, ValueError):
                high = 0
                low = 0

            buyVolume = entry[x]["uniqueBuys"] * (high + low) / 2
            sellVolume = entry[x]["uniqueSells"] * (high + low) / 2

            try:
                averageBuySize = float(entry[x]["volume"]) / entry[x]["txnCount"]
            except (ZeroDivisionError, ValueError, TypeError):
                averageBuySize = "N/A"
                
            #try:
            #    averageBuySellDelta = averageBuySize - averageSellSize
            #except (ZeroDivisionError, ValueError, TypeError):
            #    averageBuySellDelta = "N/A"

            try:
                netFlowImbalance = ((buyVolume - sellVolume) / float(entry[x]["volume"])) * 100
            except (ZeroDivisionError, ValueError, TypeError):
                netFlowImbalance = "N/A"

            try:
                uniqueBuySell = entry[x]["uniqueBuys"] / entry[x]["uniqueSells"]
            except (ZeroDivisionError, ValueError, TypeError):
                uniqueBuySell = "N/A"

            try:
                retention = (entry[x]["buyCount"] - entry[x]["uniqueBuys"]) / entry[x]["txnCount"] * 100
            except (ZeroDivisionError, ValueError, TypeError):
                retention = "N/A"

            try:
                buyVolumeDom = (buyVolume / (buyVolume + sellVolume)) * 100
            except (ZeroDivisionError, ValueError, TypeError):
                buyVolumeDom = "N/A"

            #volume = float(entry[x]["volume"])
            #volumeChange = float(entry[x]["volumeChange"])
            
            if entry["isScam"]:
                scam = "High"
            else:
                scam = "Low"

            results = {"avgBuy": averageBuySize,
                       #"avgBuySellDelta": averageBuySellDelta,
                       "buyVolumeDom": buyVolumeDom,
                       "uBuySell": uniqueBuySell,
                       "retention": retention,
                       "walletsUnder1Day": entry["swapPct1dOldWallet"],
                       "risk": scam,
                       "netFlowImbalance": netFlowImbalance}

            final[str(x)] = results

    print(final)
    return final
