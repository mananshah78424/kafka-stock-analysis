import requests

headers = {
    'Content-Type': 'application/json'
}
requestResponse = requests.get("https://api.tiingo.com/tiingo/crypto/prices?tickers=btcusd&startDate=2024-08-08&resampleFreq=5min&token=05e81df984e988bfdccfbd00bbbe05019f33e61b", headers=headers)
print(requestResponse.json())