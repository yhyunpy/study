# %%
import requests


def get_upbit_btc_price_krw():
    url = "https://api.upbit.com/v1/ticker?markets=KRW-BTC"
    response = requests.get(url)
    data = response.json()
    return data[0]["trade_price"]


def krw_to_btc(krw: float, btc_price_krw: float) -> float:
    btc_amount = krw * 10000 / btc_price_krw
    return btc_amount


def btc_to_krw(btc_amount: float, btc_price_krw: float) -> float:
    return btc_amount * btc_price_krw


my_krw = 1000
btc_can_buy = krw_to_btc(my_krw, get_upbit_btc_price_krw())
print(f"{my_krw}만원 = {btc_can_buy} BTC")

my_btc = 0.1
krw_can_buy = btc_to_krw(my_btc, get_upbit_btc_price_krw())
print(f"{my_btc}BTC = {krw_can_buy:,.0f}원")

# %%
