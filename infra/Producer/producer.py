import time
import json
import requests
from kafka import KafkaProducer

API_KEY = "d3qh70pr01quv7kar7g0d3qh70pr01quv7kar7gg"
BASE_URL = "https://finnhub.io/api/v1/quote"
SYMBOLS = ['AAPL','MSFT','TSLA']
PARTITION_MAP = {
    'AAPL': 0,
    'MSFT': 1,
    'TSLA': 2
}


producer = KafkaProducer(
    bootstrap_servers = ['localhost:29092'],
    value_serializer = lambda v: json.dumps(v).encode('utf-8'),
    max_request_size=200000000
    )

producer.send('stock-quotes', value={"symbol":"TEST","price":100}, key=b"TEST")
print("here")

def fetch_quote(symbol):
    url = f'{BASE_URL}?symbol={symbol}&token={API_KEY}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        data['symbol'] = symbol
        data['fetched_at'] = int(time.time())
        return data
    except Exception as e:
        print(f'Error fetching {symbol}: {e} ')
        return None

while True:
    for symbol in SYMBOLS:
        quote = fetch_quote(symbol)
        partition = PARTITION_MAP[symbol]
        serialized = json.dumps(quote).encode('utf-8')
        print(f"{symbol} payload size: {len(serialized)} bytes")
        if quote:
            print(f'Producing {quote}')
            producer.send('stock-quotes',value=quote)
            print('sent')
            
    producer.flush()
    time.sleep(6)    
    