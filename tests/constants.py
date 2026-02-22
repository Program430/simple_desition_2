import json


FILE_NAME = "tests/data/ticker_prices.jsonl"
TOTAL_COUNT_BTC = 0
TOTAL_COUNT_ETH = 0
BTC = "btc_usd"
ETH = "eth_usd"


with open(FILE_NAME) as file:
    for line in file:
        if not line:
            continue
        
        ticker_price_dict = json.loads(line)
        
        ticker = ticker_price_dict["ticker"]
        
        if ticker == BTC:
            TOTAL_COUNT_BTC += 1
            
        if ticker == ETH:
            TOTAL_COUNT_ETH += 1
    

            

    
        