# app.py
# iPad / Pyto compatible stock + FX checker
# No yfinance required

import requests

# -----------------------------
# SETTINGS
# -----------------------------
ticker = "ARM"          # Arm Holdings
shares = 1335
usd_to_gbp_fallback = 0.79

# -----------------------------
# FUNCTIONS
# -----------------------------
def get_stock_price(symbol):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    r = requests.get(url)
    data = r.json()

    meta = data["chart"]["result"][0]["meta"]
    return meta["regularMarketPrice"], meta["currency"]


def get_fx_rate():
    try:
        url = "https://open.er-api.com/v6/latest/USD"
        r = requests.get(url)
        data = r.json()
        return data["rates"]["GBP"]
    except:
        return usd_to_gbp_fallback


# -----------------------------
# MAIN
# -----------------------------
try:
    stock_price, currency = get_stock_price(ticker)
    fx_rate = get_fx_rate()

    total_usd = stock_price * shares
    total_gbp = total_usd * fx_rate

    print("------ STOCK SUMMARY ------")
    print("Ticker:", ticker)
    print("Share Price:", round(stock_price, 2), currency)
    print("Shares:", shares)
    print("Total Value USD:", round(total_usd, 2))
    print("USD to GBP:", round(fx_rate, 4))
    print("Total Value GBP:", round(total_gbp, 2))

except Exception as e:
    print("Error:", e)