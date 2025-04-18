def calculate_metrics(entry):

    final = {}

    for x in entry:
        if x != "priceUSD":
            try:
                high = float(entry[x]["high"])
                low = float(entry[x]["low"])
            except (TypeError, ValueError):
                high = 0
                low = 0

            buyVolume = entry[x]["uniqueBuys"] * (high + low) / 2
            sellVolume = entry[x]["uniqueSells"] * (high + low) / 2

            try:
                averageBuySize = float(entry[x]["volume"]) / entry[x]["buyCount"]
            except (ZeroDivisionError, ValueError, TypeError):
                averageBuySize = "N/A"
                
            try:
                averageSellSize = float(entry[x]["volume"]) / entry[x]["sellCount"]
            except (ZeroDivisionError, ValueError, TypeError):
                averageSellSize = "N/A"

            try:
                averageBuySellDelta = averageBuySize - averageSellSize
            except (ZeroDivisionError, ValueError, TypeError):
                averageBuySellDelta = "N/A"

            try:
                uniqueBuySell = entry[x]["uniqueBuys"] / entry[x]["uniqueSells"]
            except (ZeroDivisionError, ValueError, TypeError):
                uniqueBuySell = "N/A"

            try:
                retention = (entry[x]["buyCount"] - entry[x]["uniqueBuys"]) / entry[x]["txnCount"] * 100
            except (ZeroDivisionError, ValueError, TypeError):
                retention = "N/A"

            try:
                netBuySell = buyVolume / (buyVolume + sellVolume) * 100
            except (ZeroDivisionError, ValueError, TypeError):
                netBuySell = "N/A"

            volume = float(entry[x]["volume"])
            volumeChange = float(entry[x]["volumeChange"])

            results = {"avgBuy": averageBuySize,
                       "avgSell": averageSellSize,
                       "avgBuySellDelta": averageBuySellDelta,
                       "volume": volume,
                       "volumeChange": volumeChange,
                       "uBuySell": uniqueBuySell,
                       "retention": retention,
                       "nBuySell": netBuySell}

            final[str(x)] = results

    print(final)
    return final
