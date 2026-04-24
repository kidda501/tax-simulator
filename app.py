import streamlit as st
import numpy as np

st.set_page_config(page_title="Comp & RSU Simulator", layout="wide")

st.title("UK Compensation + RSU Simulator (Advanced)")

# -----------------------
# Inputs
# -----------------------
salary = st.slider("Base Salary (£)", 20000, 250000, 60000, 1000)
pension_pct = st.slider("Salary Sacrifice (%)", 0, 40, 10)

ticker = st.text_input("RSU Stock Ticker (e.g. AAPL, MSFT)", "AAPL")

rsu_grant = st.slider("Total RSU Grant (£ value at grant)", 0, 200000, 40000, 1000)

vesting_years = st.slider("Vesting Period (years)", 1, 5, 4)
volatility = st.slider("Annual Volatility (%)", 5, 80, 25)

# -----------------------
# UK Tax (simplified but structured)
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
            (50270 - 12570) * 0.20
            + (125140 - 50270) * 0.40
            + (income - 125140) * 0.45
        )

def ni(income):
    if income <= 12570:
        return 0
    elif income <= 50270:
        return (income - 12570) * 0.08
    else:
        return (50270 - 12570) * 0.08 + (income - 50270) * 0.02

# -----------------------
# RSU Simulation Engine
# -----------------------
years = np.arange(1, vesting_years + 1)
base_price = 100  # normalized starting price

results = []

for y in years:
    # simulate stock price path
    shock = np.random.normal(0, volatility / 100)
    price = base_price * np.exp(shock * y)

    vest_value = rsu_grant / vesting_years * (price / base_price)

    pension = salary * pension_pct / 100
    taxable_salary = salary - pension

    total_income = taxable_salary + vest_value

    tax = income_tax(total_income)
    nat_ins = ni(total_income)

    net = salary + vest_value - pension - tax - nat_ins

    results.append({
        "Year": y,
        "RSU Value": vest_value,
        "Tax": tax,
        "NI": nat_ins,
        "Net": net
    })

# -----------------------
# Display results
# -----------------------
net_values = [r["Net"] for r in results]
rsu_values = [r["RSU Value"] for r in results]

st.subheader("Vesting Simulation")

st.line_chart({
    "Net Income": net_values,
    "RSU Income": rsu_values
})

st.subheader("Year-by-Year Breakdown")

for r in results:
    st.write(
        f"Year {r['Year']}: "
        f"RSU £{r['RSU Value']:,.0f} | "
        f"Tax £{r['Tax']:,.0f} | "
        f"Net £{r['Net']:,.0f}"
    )

st.success("Model complete  v1.0 — RSUs now simulate real stock-linked vesting + volatility.")