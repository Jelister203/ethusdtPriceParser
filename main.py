import json
from scipy.stats import pearsonr
import requests
import time


def parsePrice(symbol: str = "ETHUSDT") -> float:
    url: str = f'https://api.binance.com/api/v1/ticker/price?symbol={symbol}'
    response = requests.get(url)
    data: dict = json.loads(response.text)
    return float(data['price'])

def pricer():
    current_price: float = parsePrice()
    prices_eth: [float] = [current_price]
    current_price = parsePrice("BTCUSDT")
    prices_btc: [float] = [current_price]
    while True:
        time.sleep(1)
        current_price = parsePrice("BTCUSDT")
        prices_btc.append(current_price)
        current_price = parsePrice()
        prices_eth.append(current_price)
        if current_price != None:
            if len(prices_eth) > 3600:
                prices_eth.pop(0)
                prices_btc.pop(0)
            price_change: float = (current_price - prices_eth[0]) / prices_eth[0] * 100
            corr: dict = pearsonr(prices_eth, prices_btc)
            if price_change >= 1:
                if abs(corr.statistic) < 0.5:
                    print(f'Цена изменилась на {price_change}% за последний час')
                else:
                    print(f'Цена изменилась на {price_change:.2f}% за последний час по влияюнию BTC')

if __name__ == "__main__":
    pricer()
