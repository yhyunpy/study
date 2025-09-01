# %%
import datetime as dt
from enum import IntEnum

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pykrx
import requests
import yfinance as yf
from bs4 import BeautifulSoup


class AssetType(IntEnum):
    CASH = 0
    """현금"""
    STOKE = 1
    """주식"""
    GOLD = 2
    """금현물"""
    BTC = 3
    """비트코인"""


def get_usd_krw_rate() -> float:
    url = "https://finance.naver.com/marketindex/?tabSel=exchange#tab_section"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    tag = soup.select_one("#exchangeList li.on span.value")
    rate = float(tag.text.replace(",", ""))
    print(f"현재 환율 : {rate} 원/달러")
    return rate


def get_stock_price(ticker: str, exchange_rate: float) -> float:
    if ticker[0].isdigit():
        url = f"https://finance.naver.com/item/main.nhn?code={ticker}"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        tag = soup.select_one("p.no_today span.blind")
        return float(tag.text.replace(",", ""))
    elif ticker[0].isalpha():
        stock = yf.Ticker(ticker)
        usd_price = stock.info.get("regularMarketPrice")
        if usd_price is None:
            raise Exception(f"INVALID TICKER : {ticker}")
        krw_price = exchange_rate * usd_price
        return float(krw_price)
    else:
        raise Exception(f"INVALID TICKER : {ticker}")


def get_gold_price() -> float:
    url = "https://finance.naver.com/marketindex/goldDetail.nhn"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    spans = soup.select("p.no_today span")
    price = float(
        "".join(
            span.text
            for span in spans
            if span.text.strip().isdigit() or span.text in ["."]
        )
    )
    print(f"현재 금 가격 : {price} 원/g")
    return price


def get_btc_price():
    url = "https://api.upbit.com/v1/ticker?markets=KRW-BTC"
    response = requests.get(url)
    data = response.json()
    price = float(data[0]["trade_price"])
    print(f"현재 비트코인 가격 : {price} 원/BTC")
    return price


def calc_krw_value(asset_df):
    asset_df["KrwValue"] = np.nan

    exchange_rate = get_usd_krw_rate()
    gold_price = get_gold_price()
    btc_price = get_btc_price()

    cash_mask = asset_df["AssetType"] == AssetType.CASH.value
    asset_df.loc[cash_mask, "KrwValue"] = asset_df.loc[cash_mask, "Amount"]

    stock_mask = asset_df["AssetType"] == AssetType.STOKE.value
    asset_df.loc[stock_mask, "KrwValue"] = asset_df.loc[stock_mask].apply(
        lambda row: row["Amount"] * get_stock_price(str(row["Ticker"]), exchange_rate),
        axis=1,
    )

    gold_mask = asset_df["AssetType"] == AssetType.GOLD.value
    asset_df.loc[gold_mask, "KrwValue"] = asset_df.loc[gold_mask].apply(
        lambda row: row["Amount"] * gold_price, axis=1
    )

    btc_mask = asset_df["AssetType"] == AssetType.BTC.value
    asset_df.loc[btc_mask, "KrwValue"] = asset_df.loc[btc_mask].apply(
        lambda row: row["Amount"] * btc_price, axis=1
    )

    return asset_df


def autopct_format(pct):
    return f"{pct:.1f}%" if pct > 0 else ""


def show_asset_type_pie(asset_df: pd.DataFrame):
    summary = (
        asset_df.groupby("AssetType")["KrwValue"]
        .sum()
        .rename(index=lambda x: AssetType(x).name)
        .sort_values(ascending=False)
    )

    def autopct_format(pct, allvals):
        if pct < 1:
            return ""
        absolute = int(round(pct / 100.0 * np.sum(allvals))) / 10000
        return f"{pct:.1f}%\n({absolute:,.0f}만)"

    plt.figure(figsize=(8, 8))
    plt.rcParams["font.family"] = "AppleGothic"
    summary.plot.pie(
        autopct=lambda pct: autopct_format(pct, summary),
        startangle=90,
        counterclock=False,
    )
    plt.title("자산 종류별 비중")
    plt.ylabel("")
    plt.show()


def show_stock_pie(asset_df: pd.DataFrame):
    def ticker_to_group(ticker):
        if ticker in ["VOO", "360200"]:
            return "VOO"
        elif ticker in ["QQQ", "367380"]:
            return "QQQ"
        elif ticker in ["SCHD", "458730"]:
            return "SCHD"
        else:
            return ticker

    stock_df = asset_df.loc[asset_df["AssetType"] == AssetType.STOKE.value].copy()
    stock_df["TickerGroup"] = stock_df["Ticker"].apply(ticker_to_group)

    summary = stock_df.groupby("TickerGroup")["KrwValue"].sum()

    total = summary.sum()
    group_labels = {}
    for group, value in summary.items():
        if value / total < 0.05:
            group_labels[group] = "ETC"
        else:
            group_labels[group] = group
    summary.index = summary.index.map(lambda x: group_labels[x])
    summary = summary.groupby(summary.index).sum().sort_values(ascending=False)

    def autopct_format(pct, allvals):
        absolute = int(round(pct / 100.0 * np.sum(allvals))) / 10000
        return f"{pct:.1f}%\n({absolute:,.0f}만)"

    plt.figure(figsize=(8, 8))
    summary.plot.pie(
        autopct=lambda pct: autopct_format(pct, summary),
        startangle=90,
        counterclock=False,
    )
    plt.title("주식 종목별 비중")
    plt.ylabel("")
    plt.tight_layout()
    plt.show()


# %%
asset_df = pd.read_csv("asset.csv")
asset_df = calc_krw_value(asset_df)
show_asset_type_pie(asset_df)
show_stock_pie(asset_df)

# %%
