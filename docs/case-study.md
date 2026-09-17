# Case Study — Sales Compensation Forecasting & Accrual Intelligence

## Business Problem

Sales-compensation forecasting often breaks because several different questions are mixed together:

1. How much variable compensation could the plan produce?
2. How much commission is expected to be earned?
3. How much of earned commissions should hit P&L this year?
4. How much cash will actually be paid this year?
5. How do accelerators and renewal gates change the economics at high attainment?

A single percentage assumption cannot answer all five reliably.

## Solution

This public demo separates the model into four layers:

- **Top-down planning** — variable potential, merit, investments, accelerators, achievement
- **Bottom-up economics** — revenue drivers, services, renewal bonuses, and net accelerators
- **Accounting** — capitalization and prior-cohort amortization
- **Cash timing** — payout timing modeled independently from expense recognition

## Controls

The model treats assumptions as explicit inputs rather than hidden balancing items. The public example also keeps top-down and bottom-up methods side by side so management can see where the forecast methods diverge.

## Accelerator Logic

The demo includes a fictional nonlinear payline solely to demonstrate why commissions can accelerate faster than bookings after quota. The public rates are intentionally not copied from any employer compensation plan.

## Public-Safe Rebuild

The original analytical exercise contained company-specific business units, internal source references, actual financial values, and plan-policy details. Those items are excluded here. The public version preserves only the architecture, accounting concepts, control design, and modeling patterns.
