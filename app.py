import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from core import CommissionInputs, top_down, bottom_up, payline_table, scenario_table

st.set_page_config(page_title="Sales Commission Forecasting Engine", layout="wide")
st.title("Sales Compensation Forecasting & Accrual Intelligence")
st.caption("Synthetic public demonstration — driver-based forecasting, accelerator simulation, accounting treatment, and cash planning.")

with st.sidebar:
    st.header("Scenario levers")
    achievement = st.slider("Plan achievement", 0.70, 1.05, 0.90, 0.01)
    baseline = st.number_input("Baseline variable potential ($M)", 10.0, 40.0, 22.4, 0.1) * 1_000_000
    merit = st.number_input("Merit increase ($M)", 0.0, 5.0, 0.62, 0.05) * 1_000_000
    investment = st.number_input("Investment potential ($M)", 0.0, 8.0, 1.05, 0.05) * 1_000_000
    accel_pool = st.number_input("Accelerator pool ($M)", 0.0, 10.0, 2.85, 0.05) * 1_000_000
    cap_rate = st.slider("Capitalization rate", 0.30, 0.65, 0.48, 0.01)
    amort = st.number_input("Prior-cohort amortization ($M)", 0.0, 15.0, 8.2, 0.1) * 1_000_000
    cash_ratio = st.slider("Cash / earned ratio", 0.85, 1.25, 1.07, 0.01)

inp = CommissionInputs(
    baseline_potential=baseline,
    merit_increase=merit,
    investment_potential=investment,
    accelerator_pool=accel_pool,
    achievement=achievement,
    capitalization_rate=cap_rate,
    prior_cohort_amortization=amort,
    cash_to_earned=cash_ratio,
)

td = top_down(inp)
bu = bottom_up(inp)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Variable Potential", f"${td['total_variable_potential']/1e6:,.1f}M")
c2.metric("Top-Down Earned", f"${td['earned']/1e6:,.1f}M")
c3.metric("P&L Expense", f"${td['expense']/1e6:,.1f}M")
c4.metric("Cash Out", f"${td['cash']/1e6:,.1f}M")

st.subheader("Top-down commission bridge")
steps = [
    ("Baseline", inp.baseline_potential),
    ("Merit", inp.merit_increase),
    ("Investment", inp.investment_potential),
    ("Accelerators", inp.accelerator_pool),
    ("Achievement Adj.", td['earned'] - td['total_variable_potential']),
    ("Capitalization", td['capitalized']),
    ("Prior Amortization", td['prior_amortization']),
]
fig = go.Figure(go.Waterfall(
    x=[x[0] for x in steps] + ["P&L Expense"],
    measure=["relative"] * len(steps) + ["total"],
    y=[x[1] for x in steps] + [td['expense']],
    connector={"line": {"width": 1}},
))
fig.update_layout(yaxis_title="$", showlegend=False)
st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Top-down vs bottom-up")
    compare = pd.DataFrame({
        "Method": ["Top-down", "Bottom-up"],
        "Commissions Earned": [td['earned'], bu['earned']],
        "P&L Expense": [td['expense'], bu['expense']],
        "Cash": [td['cash'], bu['cash']],
    })
    st.plotly_chart(px.bar(compare, x="Method", y=["Commissions Earned", "P&L Expense", "Cash"], barmode="group"), use_container_width=True)
    st.caption("Bottom-up is intentionally built from separate revenue, services, renewal, and accelerator drivers rather than a single achievement assumption.")

with right:
    st.subheader("Bottom-up components")
    components = pd.DataFrame({
        "Component": ["Revenue", "Services", "Early Renewal", "Net Accelerators"],
        "Value": [bu['revenue_component'], bu['services_component'], bu['early_renewal_bonus'], bu['net_accelerators']],
    })
    st.plotly_chart(px.bar(components, x="Component", y="Value"), use_container_width=True)
    st.metric("Bottom-up unit cost", f"{bu['unit_cost']:.1%}")

st.subheader("Synthetic accelerator mechanics")
pay = payline_table()
pay["attainment_pct"] = pay["attainment"] * 100
pay["incentive_pct"] = pay["target_incentive_earned"] * 100
st.plotly_chart(px.line(pay, x="attainment_pct", y="incentive_pct", markers=True, labels={"attainment_pct":"Quota attainment %", "incentive_pct":"Target incentive earned %"}), use_container_width=True)
st.caption("Public demo policy: 1.0× through quota, 2.5× from 100%–150%, and 1.25× above 150%. These are fictional rates used only to demonstrate nonlinear payout mechanics.")

st.subheader("Scenario range")
sc = scenario_table(inp)
sc_display = sc.copy()
sc_display["achievement"] = (sc_display["achievement"] * 100).round(1)
st.plotly_chart(px.scatter(sc, x="earned", y="expense", size="cash", text="scenario", hover_data=["achievement"]), use_container_width=True)
st.dataframe(sc_display, use_container_width=True, hide_index=True)

st.subheader("Control & accounting interpretation")
st.info(
    f"At {achievement:.0%} achievement, the top-down model earns ${td['earned']/1e6:,.1f}M. "
    f"With {cap_rate:.0%} capitalized, ${td['current_year_expense']/1e6:,.1f}M hits current-year expense before "
    f"${td['prior_amortization']/1e6:,.1f}M of prior-cohort amortization. Cash is modeled separately at {cash_ratio:.2f}× earned."
)
