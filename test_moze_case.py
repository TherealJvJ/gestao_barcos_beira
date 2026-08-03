import requests

url = "https://api.mozesms.com/v1/sms/send"
api_key = "mk_d6c25aac338e71c7dbb83c11a3f373d1"
api_secret = "sk_246ccf7af9dbffa7284deb0e0246157b185feff06782f4b071ff3d1cb420b367"

# Teste com ESHOP (aprovado na conta)
print("--- Teste com Sender ID: ESHOP ---")
try:
    resp = requests.post(url, json={"to": "258869196190", "message": "INTRANSMAR: Teste de envio de SMS. Se recebeu esta mensagem, o sistema esta funcional!", "from": "ESHOP"}, headers={"X-API-Key": api_key, "X-API-Secret": api_secret}, timeout=30)
    print(f"Status: {resp.status_code}")
    print(f"Body: {resp.text}")
except Exception as e:
    print(f"Erro: {e}")
