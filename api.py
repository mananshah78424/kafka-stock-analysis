from json import dumps

import requests

api_key = 'f06361252d124e0892a0de996098608d'
interval = '1day'
symbols=['IBM','AAPL']

urls = [f'https://api.twelvedata.com/time_series?symbol={symbol}&interval={interval}&apikey={api_key}&outputsize=1' for symbol in symbols]
def fetch_data(url):
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        symbol=data["meta"]["symbol"]
        for value in data["values"]:
            my_data={"symbol":symbol,"open":value["open"],"date":value["datetime"]}
            
    else:
        print(f"Error fetching data from {url}: {data.get('message', 'Unknown error')}")
        return None

if __name__ == "__main__":
    for url in urls:
        data = fetch_data(url)
        if data:
            print(f"Data for URL {url}:")
            print(dumps(data, indent=2))  # Pretty-print JSON data