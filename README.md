# Sales Compensation Forecasting & Accrual Intelligence

**[Launch the live demo](https://sales-commission-forecasting-engine.onrender.com)**

A public-safe, interactive reference implementation for driver-based sales commission forecasting, policy simulation, capitalization/amortization accounting, and cash planning.

> **Portfolio note:** This demo is inspired by enterprise FP&A and sales-compensation planning patterns, but all company names, business-unit labels, rates, policies, and financial values used here are synthetic. No employer data, credentials, internal identifiers, or proprietary source files are included.

## What this demo proves

- Top-down commission planning from baseline variable potential, merit, investments, accelerators, and achievement
- Bottom-up commission forecasting from bookings / recurring-revenue drivers, services, and policy mechanics
- Accelerator and payline simulation
- Commission-earned to P&L expense bridge
- Capitalization and amortization treatment
- Cash payout timing
- Scenario and sensitivity analysis
- Explicit separation of sourced calculations, assumptions, and management allocations

## Public Demo Architecture

```text
Synthetic Sales / Revenue Drivers
              |
              v
      Commission Policy Engine
              |
      +-------+--------+
      |                |
      v                v
 Top-Down Plan     Bottom-Up Build
      |                |
      +-------+--------+
              |
       Commissions Earned
              |
      Capitalization / Amortization
              |
          P&L Expense
              |
          Cash Timing
              |
       Scenario Dashboard
```

## Technology

`Python` `Streamlit` `Pandas` `Plotly` `FP&A` `Sales Compensation` `ASC 340-40` `Scenario Modeling`

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Repository Structure

```text
.
├── app.py
├── core.py
├── requirements.txt
├── render.yaml
├── docs/
│   └── case-study.md
└── tests/
    └── test_core.py
```

## Design Principle

The demo deliberately distinguishes **forecasting logic**, **accounting treatment**, and **cash timing**. It also labels assumptions instead of hiding them inside balancing plugs.
