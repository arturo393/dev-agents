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
print("🔍 Analizando Transaction Log (Últimas 50 transacciones)...")
payload = "accountType=UNIFIED&category=linear&limit=50"
res = HTTP_Request('/v5/account/transaction-log', 'GET', payload)

if res.get('retCode') == 0:
    logs = res['result']['list']
    funding_total = 0
    trade_fee_total = 0
    realized_pnl_total = 0
    
    for item in logs:
        change = float(item['change'] or 0)
        type_str = item.get('type', '')
        
        if "Funding" in type_str:
            funding_total += change
        elif "Trade" in type_str:
            trade_fee_total += change
        elif "RealizedPnL" in type_str:
            realized_pnl_total += change
            
    print(f"\n📊 RESUMEN DE FLUJO DE CAJA (Last 50 events):")
    print(f"✅ Ganancia/Pérdida por Trades: ${realized_pnl_total:.4f}")
    print(f"💸 Comisiones de Ejecución:      ${trade_fee_total:.4f}")
    print(f"🩸 Drenaje por Funding Fees:     ${funding_total:.4f}")
    print(f"-------------------------------------------")
    total_impact = realized_pnl_total + trade_fee_total + funding_total
    print(f"📉 Impacto Neto Real en Balance: ${total_impact:.4f}")
else:
    print("Error:", res)
