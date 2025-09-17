# Webhook-tradingview-bitkub-api
## BITKUB API WEBHOOK
#Check balance:
```
curl -X GET http://localhost:8899/balance \
  -H "X-API-KEY: your-secret-api-key"

```

#Place order:
```
curl -X POST http://localhost:8899/order \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: your-secret-api-key" \
  -d '{"symbol":"btc_thb","side":"buy","amt":0.001,"rat":1200000,"typ":"limit"}'
```

#TradingView webhook → http://<server_ip>:8899/webhook
```
{"cmd":"buy","symbol":"btc_thb","amt":0.001,"rat":1200000,"typ":"limit"}
```
