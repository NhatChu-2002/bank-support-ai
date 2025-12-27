import requests
from typing import Any, Dict

def send_message(api_url: str, customer_name: str, message: str, timeout: int = 15) -> Dict[str, Any]:
    payload = {"customer_name": customer_name, "message": message}
    resp = requests.post(api_url, json=payload, timeout=timeout)
    resp.raise_for_status()
    return resp.json()
