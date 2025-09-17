import os
import time
import json
import hmac
import hashlib
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BITKUB_API_KEY")
API_SECRET = os.getenv("BITKUB_API_SECRET")
HOST = "https://api.bitkub.com"

def gen_sign(api_secret, payload_string):
    return hmac.new(api_secret.encode("utf-8"), payload_string.encode("utf-8"), hashlib.sha256).hexdigest()

def private_request(method, path, body=None):
    ts = str(round(time.time() * 1000))
    payload = [ts, method, path, json.dumps(body) if body else ""]
    sig = gen_sign(API_SECRET, "".join(payload))

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-BTK-TIMESTAMP": ts,
        "X-BTK-SIGN": sig,
        "X-BTK-APIKEY": API_KEY
    }
    url = HOST + path
    resp = requests.request(method, url, headers=headers, data=json.dumps(body) if body else None, verify=True)
    return resp.json()

# ==== API FUNCTIONS ====

def get_balances():
    return private_request("POST", "/api/v3/market/wallet")

def place_order(symbol, side, amt, rat=None, typ="limit"):
    """
    side: "buy" or "sell"
    typ: "limit" or "market"
    """
    path = "/api/v3/market/place-bid" if side == "buy" else "/api/v3/market/place-ask"
    body = {
        "sym": symbol,   # e.g. btc_thb
        "amt": amt,      # amount in base coin
        "typ": typ
    }
    if typ == "limit" and rat:
        body["rat"] = rat
    return private_request("POST", path, body)
