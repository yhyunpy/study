# %%
import os
import pprint
import requests

import pandas as pd
from dotenv import load_dotenv

load_dotenv("local.env")


class Upbit:
    def __init__(self):
        self.pub_key = os.getenv("UPBIT_PUB_KEY", None)
        self.secret_key = os.getenv("UPBIT_SECRET_KEY", None)
        self.headers = {"accept": "application/json"}

    def get_btc_krw_price(self):
        markets = "KRW-BTC"
        url = f"https://api.upbit.com/v1/ticker?markets={markets}"
        response = requests.get(url, headers=self.headers)
        return response.text

    def get_btc_krw_daily_chart(self):
        url = "https://api.upbit.com/v1/candles/days"
        response = requests.get(url, headers=self.headers)
        return response.text


# %%
Upbit().get_btc_krw_price()

# %%
