from flask import Flask, request, jsonify
from bitkub_api import get_balances, place_order

app = Flask(__name__)

# ====== ตั้งค่า API KEY ======
API_KEY = "gMXEJ2RvUVRmuaFaFfMr"

def require_api_key(func):
    """Decorator สำหรับตรวจสอบ API Key"""
    def wrapper(*args, **kwargs):
        key = request.headers.get("X-API-KEY")
        if not key or key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@app.route("/")
def index():
    return {"status": "Bitkub Trading API running"}

@app.route("/balance", methods=["GET"])
@require_api_key
def balance():
    return jsonify(get_balances())

@app.route("/order", methods=["POST"])
@require_api_key
def order():
    data = request.json
    symbol = data.get("symbol", "btc_thb")
    side = data.get("side", "buy")   # "buy" or "sell"
    amt = data.get("amt", 0.001)
    rat = data.get("rat")            # price for limit
    typ = data.get("typ", "limit")

    return jsonify(place_order(symbol, side, amt, rat, typ))

# === Webhook for TradingView ===
@app.route("/webhook", methods=["POST"])
@require_api_key
def webhook():
    data = request.json
    print("Webhook received:", data)

    # TradingView payload example:
    # {"cmd":"buy","symbol":"btc_thb","amt":0.001,"rat":1200000,"typ":"limit"}

    cmd = data.get("cmd")
    symbol = data.get("symbol", "btc_thb")
    amt = data.get("amt", 0.001)
    rat = data.get("rat")
    typ = data.get("typ", "limit")

    if cmd == "buy":
        result = place_order(symbol, "buy", amt, rat, typ)
    elif cmd == "sell":
        result = place_order(symbol, "sell", amt, rat, typ)
    else:
        result = {"error": "Invalid command"}

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8899)
