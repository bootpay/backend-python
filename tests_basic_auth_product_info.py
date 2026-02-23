import base64
import os
import requests

client_key = os.getenv('BP_CLIENT_KEY', 'QIzXk4M3EeD-6B1GTfmGHA')
secret_key = os.getenv('BP_SECRET_KEY', 'vRle44QfyBj7nzJlBbeebqkbtlJVRTS2DQa9Adpz3d8=')
base_url = os.getenv('BP_BASE_URL', 'https://dev-api.bootapi.com/v1')

encoded = base64.b64encode(f"{client_key}:{secret_key}".encode()).decode()
headers = {
    'Authorization': f'Basic {encoded}',
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'bootpay_api_version': '5.0.0',
    'bootpay_sdk_version': '5.0.0',
    'bootpay_sdk_type': '300',
}

resp = requests.get(f"{base_url}/products?page=1&limit=1", headers=headers, timeout=20)
print({'status': resp.status_code, 'ok': resp.ok, 'preview': resp.text[:500]})
if not resp.ok:
    raise SystemExit(1)
