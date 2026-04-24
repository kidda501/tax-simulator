import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="RSU FX Tax Model", layout="wide")

st.title("ARM RSU + UK Tax Simulator (USD → GBP Real Model)")

# -----------------------
# LIVE DATA
# -----------------------
ticker = "ARM"
fx_pair = "GBP=X"   # USD → GBP

@st.cache_data(ttl=60)
def get_price(t):
    return yf.Ticker(t).history(period="1d")["Close"].iloc[-1]

try:
    arm_price_usd = get_price(ticker)
except:
    arm_price_usd = 100

try:
    fx = get_price(fx_pair)  # USD per GBP
    usd_to_gbp = 1 / fx
except:
    usd_to_gbp = 0.79  # fallback

st.metric("ARM Price (USD)", f"${arm_price_usd:.2f}")
st.metric("USD → GBP FX Rate", f"£{usd_to_gbp:.4f}")

# -----------------------
# INPUTS
# -----------------------
total_shares = 1335
salary = st.slider("Base Salary (£)", 20000, 250000, 60000, 1000)
pension_pct = st.slider("Salary Sacrifice (%)", 0, 40, 10)

# -----------------------
# VESTING STRUCTURE
# -----------------------
vest_42 = 0.42
vest_6 = 0.06
vest_4 = 0.04

shares_2026 = total_shares * vest_42

# USD value of RSUs at vest
rsu_value_usd = shares_2026 * arm_price_usd

# convert to GBP for UK tax
rsu_value_gbp = rsu_value_usd * usd_to_gbp

# -----------------------
# TAX ENGINE (UK)
# -----------------------
def income_tax(income):
    if income <= 12570:
        return 0
    elif income <= 50270:
        return (income - 12570) * 0.20
    elif income <= 125140:
        return (50270 - 12570) * 0.20 + (income - 50270) * 0.40
    else:
        return (
            (50270 - 12570) * 0.20 +
            (125140 - 50270) * 0.40 +
            (income - 125140) * 0.45
        )

def ni(income):
    if income <= 12570:
        return 0
    elif income <= 50270:
        return (income - 12570) * 0.08
    else:
        return (50270 - 12570) * 0.08 + (income - 50270) * 0.02

# -----------------------
# SALARY + RSU TAX MODEL
# -----------------------
pension = salary * pension_pct / 100
taxable_salary = salary - pension

total_income = taxable_salary + rsu_value_gbp

tax = income_tax(total_income)
nat_ins = ni(taxable_salary)

net = salary + rsu_value_gbp - pension - tax - nat_ins

# -----------------------
# OUTPUT
# -----------------------
st.subheader("2026 Vesting (42% tranche only)")

col1, col2, col3 = st.columns(3)

col1.metric("RSU Value (USD)", f"${rsu_value_usd:,.0f}")
col2.metric("RSU Value (GBP)", f"£{rsu_value_gbp:,.0f}")
col3.metric("Net Income (2026)", f"£{net:,.0f}")

st.divider()

st.subheader("Tax Breakdown (UK)")

st.write(f"Taxable Income: £{total_income:,.0f}")
st.write(f"Income Tax: £{tax:,.0f}")
st.write(f"National Insurance: £{nat_ins:,.0f}")

st.divider()

st.subheader("Full Vesting Context (not taxed yet)")

df = pd.DataFrame({
    "Vesting Bucket": ["42% Aug 2026", "6% × 7 quarters", "4% × 4 quarters"],
    "Shares": [
        shares_2026,
        total_shares * vest_6 * 7,
        total_shares * vest_4 * 4
    ]
})

df["USD Value"] = df["Shares"] * arm_price_usd
df["GBP Value"] = df["USD Value"] * usd_to_gbp

st.dataframe(df)

st.caption("RSUs v1.0 taxed at vesting: USD value converted to GBP using live FX rate.")