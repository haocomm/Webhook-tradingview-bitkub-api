## BITKUB API WEBHOOK
#Check balance:
```
curl http://localhost:8899/balance
```

#Place order:
```
curl -X POST http://localhost:8899/order \
  -H "Content-Type: application/json" \
  -d '{"symbol":"btc_thb","side":"buy","amt":0.001,"rat":1200000,"typ":"limit"}'
```

#TradingView webhook → http://<server_ip>:8899/webhook
```
{"cmd":"buy","symbol":"btc_thb","amt":0.001,"rat":1200000,"typ":"limit"}
```
