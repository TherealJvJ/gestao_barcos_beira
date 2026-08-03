import requests

url = "https://api.mozesms.com/v1/sms/send"
api_key = "mk_d6c25aac338e71c7dbb83c11a3f373d1"
api_secret = "SK_246CCF7AF9DBFFA7284DEB0E0246157B185FEFF06782F4B071FF3D1CB420B367"

phone = "258841234567"
msg = "Teste INTRANSMAR"

print("--- Teste 1: Payload na raiz (api_key) ---")
try:
    resp = requests.post(url, json={"api_key": api_key, "api_secret": api_secret, "to": phone, "message": msg, "from": "MozeSMS"}, timeout=10)
    print(f"Status: {resp.status_code}, Body: {resp.text}")
except Exception as e: print(e)

print("\n--- Teste 2: Basic Auth ---")
try:
    resp = requests.post(url, json={"to": phone, "message": msg, "from": "MozeSMS"}, auth=(api_key, api_secret), timeout=10)
    print(f"Status: {resp.status_code}, Body: {resp.text}")
except Exception as e: print(e)

print("\n--- Teste 3: Bearer Token ---")
try:
    resp = requests.post(url, json={"to": phone, "message": msg, "from": "MozeSMS"}, headers={"Authorization": f"Bearer {api_key}"}, timeout=10)
    print(f"Status: {resp.status_code}, Body: {resp.text}")
except Exception as e: print(e)

print("\n--- Teste 4: API Key header custom (apikey) ---")
try:
    resp = requests.post(url, json={"to": phone, "message": msg, "from": "MozeSMS"}, headers={"apikey": api_key}, timeout=10)
    print(f"Status: {resp.status_code}, Body: {resp.text}")
except Exception as e: print(e)

print("\n--- Teste 5: Endpoint v2 ---")
try:
    resp = requests.post("https://api.mozesms.com/v2/sms/send", json={"to": phone, "message": msg, "from": "MozeSMS"}, headers={"X-API-Key": api_key, "X-API-Secret": api_secret}, timeout=10)
    print(f"Status: {resp.status_code}, Body: {resp.text}")
except Exception as e: print(e)
