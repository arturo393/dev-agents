import os
import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode

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

payload = "category=linear&limit=30"
res = HTTP_Request('/v5/position/closed-pnl', 'GET', payload)

if res.get('retCode') == 0:
    history = res['result']['list']
    total_pnl = 0
    print(f"\n--- Historial REAL de Bybit (Últimos {len(history)} movimientos) ---")
    print(f"{'Símbolo':<12} | {'Lado':<6} | {'Fecha/Hora':<20} | {'PnL/Fee ($)':<10}")
    for item in history:
        sym = item['symbol']
        side = item['side']
        pnl = float(item['closedPnl'])
        time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(item['updatedTime'])/1000))
        total_pnl += pnl
        print(f"{sym:<12} | {side:<6} | {time_str:<20} | {pnl:<10.4f}")
    
    print("---------------------------------------------------------")
    print(f"NET TOTAL ACUMULADO RECIENTE (Aprox): ${total_pnl:.4f}")
else:
    print("Error conectando a Bybit:", res)
