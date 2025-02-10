import requests
import os


COINMARKETCAP_API_KEY = os.getenv("COINMARKETCAP_API_KEY", "your-api-key")
BLOCKCHAIR_API_URL = "https://api.blockchair.com/ethereum/blocks"

def get_btc_latest_block():
    url = "https://pro-api.coinmarketcap.com/v1/blockchain/statistics/latest"
    headers = {"X-CMC_PRO_API_KEY": COINMARKETCAP_API_KEY}
    response = requests.get(url, headers=headers, params={"symbol": "BTC"})

    if response.status_code == 200:
        data = response.json()
        return data["data"]["block_height"]
    return None

def get_eth_latest_block():
    url = "https://api.blockchair.com/ethereum/blocks?q=id(desc)&limit=1"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data["data"][0]["id"]
    return None