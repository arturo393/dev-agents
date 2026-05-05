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

# fetch funding fees and trading fees (Account Log)
# Type 3 = Funding, Type 2 = Trade fee? No, let's use /v5/account/transaction-log
payload = "accountType=UNIFIED&category=linear&limit=50"
res = HTTP_Request('/v5/account/transaction-log', 'GET', payload)

if res.get('retCode') == 0:
    logs = res['result']['list']
    funding_total = 0
    trade_fee_total = 0
    print(f"\n--- Auditoría de costos invisibles (Últimos {len(logs)} registros) ---")
    for item in logs:
        change = float(item['change'])
        type_str = item['type']
        if "Funding" in type_str:
            funding_total += change
        elif "Trade" in type_str:
            trade_fee_total += change
    
    print(f"💰 Total Comisiones de Trading: ${trade_fee_total:.2f}")
    print(f"📉 Total Funding Fees (Pagos por tener posiciones abiertas): ${funding_total:.2f}")
    print(f"Total drenado en fees: ${funding_total + trade_fee_total:.2f}")
    
    if abs(funding_total) > abs(trade_fee_total):
        print("\nALERTA: El Funding Fee es tu mayor gasto. Eso confirma que las posiciones quedaron abiertas demasiado tiempo.")
else:
    print("Error:", res)
