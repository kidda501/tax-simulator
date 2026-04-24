import streamlit as st

st.set_page_config(page_title="Tax Simulator", layout="centered")

st.title("UK Salary + Tax + RSU Simulator")

salary = st.slider("Salary (£)", 20000, 250000, 60000, 1000)
pension = st.slider("Salary Sacrifice (%)", 0, 40, 10)
rsu = st.slider("RSU Income (£)", 0, 100000, 20000, 1000)
bik = st.slider("Benefits in Kind (£)", 0, 30000, 5000, 500)

# simple model (we'll improve later)
pension_amount = salary * pension / 100
taxable_income = salary - pension_amount + rsu + bik

tax = taxable_income * 0.28
ni = (salary - pension_amount) * 0.08

take_home = salary + rsu - pension_amount - tax - ni

st.subheader("Results")

st.metric("Take Home Pay", f"£{take_home:,.0f}")
st.metric("Estimated Tax", f"£{tax:,.0f}")
st.metric("Estimated NI", f"£{ni:,.0f}")
st.metric("Pension Contribution", f"£{pension_amount:,.0f}")

st.bar_chart({
    "Tax": tax,
    "NI": ni,
    "Pension": pension_amount,
    "Take Home": take_home
})
