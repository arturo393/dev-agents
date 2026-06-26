import os
import time
import hmac
import hashlib
import requests

# Parse .env
keys = {}
try:
    with open('/home/arturo/monteCarlo/.env') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                k, v = line.strip().split('=', 1)
                keys[k] = v
except FileNotFoundError:
    print("Could not find .env")
    exit(1)

api_key = keys.get('BYBIT_API_KEY')
api_secret = keys.get('BYBIT_API_SECRET')

def HTTP_Request(endPoint, method, payload):
    time_stamp = str(int(time.time() * 10 ** 3))
    recv_window = str(5000)
    param_str = str(time_stamp) + api_key + recv_window + payload
    hash = hmac.new(bytes(api_secret, "utf-8"), param_str.encode("utf-8"), hashlib.sha256)
    signature = hash.hexdigest()
    headers = {
        'X-BAPI-API-KEY': api_key,
        'X-BAPI-SIGN': signature,
        'X-BAPI-SIGN-TYPE': '2',
        'X-BAPI-TIMESTAMP': time_stamp,
        'X-BAPI-RECV-WINDOW': recv_window,
        'Content-Type': 'application/json'
    }
    url = f"https://api.bybit.com{endPoint}?{payload}" if method == "GET" else f"https://api.bybit.com{endPoint}"
    response = requests.request(method, url, headers=headers, data=payload if method=="POST" else None)
    return response.json()

print("💰 Consultando Balance TOTAL de la cuenta...")
payload = "accountType=UNIFIED"
res = HTTP_Request('/v5/account/wallet-balance', 'GET', payload)

if res.get('retCode') == 0:
    balance = res['result']['list'][0]
    total_equity = balance['totalEquity']
    total_available = balance['totalAvailableBalance']
    print(f"\n💵 TOTAL EQUITY:       ${total_equity}")
    print(f"🔓 BALANCE DISPONIBLE: ${total_available}")
    
    for coin in balance['coin']:
        if float(coin['walletBalance']) > 0:
            print(f"   - {coin['coin']}: {coin['walletBalance']}")
else:
    print("Error:", res)
