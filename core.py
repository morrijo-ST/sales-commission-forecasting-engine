from dataclasses import dataclass, asdict
import pandas as pd


@dataclass
class CommissionInputs:
    baseline_potential: float = 22_400_000
    merit_increase: float = 620_000
    investment_potential: float = 1_050_000
    accelerator_pool: float = 2_850_000
    achievement: float = 0.90
    gross_revenue_driver: float = 91_000_000
    revenue_commission_rate: float = 0.185
    services_revenue: float = 72_000_000
    services_rate: float = 0.018
    early_renewal_bonus: float = 1_150_000
    accelerator_gross: float = 4_900_000
    renewal_gate_clawback: float = 1_500_000
    capitalization_rate: float = 0.48
    prior_cohort_amortization: float = 8_200_000
    cash_to_earned: float = 1.07


def top_down(inp: CommissionInputs) -> dict:
    potential = (
        inp.baseline_potential
        + inp.merit_increase
        + inp.investment_potential
        + inp.accelerator_pool
    )
    earned = potential * inp.achievement
    current_year_expense = earned * (1 - inp.capitalization_rate)
    expense = current_year_expense + inp.prior_cohort_amortization
    cash = earned * inp.cash_to_earned
    return {
        "total_variable_potential": potential,
        "earned": earned,
        "capitalized": -earned * inp.capitalization_rate,
        "current_year_expense": current_year_expense,
        "prior_amortization": inp.prior_cohort_amortization,
        "expense": expense,
        "cash": cash,
    }


def bottom_up(inp: CommissionInputs) -> dict:
    revenue_component = inp.gross_revenue_driver * inp.revenue_commission_rate
    services_component = inp.services_revenue * inp.services_rate
    net_accelerators = inp.accelerator_gross - inp.renewal_gate_clawback
    earned = revenue_component + services_component + inp.early_renewal_bonus + net_accelerators
    capitalized = -earned * inp.capitalization_rate
    expense = earned + capitalized + inp.prior_cohort_amortization
    cash = earned * inp.cash_to_earned
    return {
        "revenue_component": revenue_component,
        "services_component": services_component,
        "early_renewal_bonus": inp.early_renewal_bonus,
        "net_accelerators": net_accelerators,
        "earned": earned,
        "capitalized": capitalized,
        "prior_amortization": inp.prior_cohort_amortization,
        "expense": expense,
        "cash": cash,
        "unit_cost": earned / inp.gross_revenue_driver,
    }


def payline(attainment: float, accel_rate: float = 2.5, tail_rate: float = 1.25) -> float:
    """Synthetic policy: 1x to quota, 2.5x from 100%-150%, 1.25x above 150%."""
    if attainment <= 1.0:
        return attainment
    if attainment <= 1.5:
        return 1.0 + (attainment - 1.0) * accel_rate
    return 1.0 + 0.5 * accel_rate + (attainment - 1.5) * tail_rate


def payline_table() -> pd.DataFrame:
    attainment = [0.80, 0.90, 1.00, 1.10, 1.20, 1.30, 1.50, 1.75, 2.00]
    return pd.DataFrame(
        {
            "attainment": attainment,
            "target_incentive_earned": [payline(x) for x in attainment],
        }
    )


def bridge(inp: CommissionInputs, method: str = "top_down") -> pd.DataFrame:
    if method == "bottom_up":
        r = bottom_up(inp)
        rows = [
            ("Revenue-driven commissions", r["revenue_component"], "movement"),
            ("Services commissions", r["services_component"], "movement"),
            ("Early-renewal bonus", r["early_renewal_bonus"], "movement"),
            ("Net accelerators", r["net_accelerators"], "movement"),
            ("Commissions earned", r["earned"], "total"),
            ("Capitalization", r["capitalized"], "movement"),
            ("Prior-cohort amortization", r["prior_amortization"], "movement"),
            ("P&L commission expense", r["expense"], "total"),
        ]
    else:
        r = top_down(inp)
        rows = [
            ("Baseline variable potential", inp.baseline_potential, "movement"),
            ("Merit increase", inp.merit_increase, "movement"),
            ("Investment potential", inp.investment_potential, "movement"),
            ("Accelerator pool", inp.accelerator_pool, "movement"),
            ("Total variable potential", r["total_variable_potential"], "total"),
            ("Achievement adjustment", r["earned"] - r["total_variable_potential"], "movement"),
            ("Commissions earned", r["earned"], "total"),
            ("Capitalization", r["capitalized"], "movement"),
            ("Prior-cohort amortization", r["prior_amortization"], "movement"),
            ("P&L commission expense", r["expense"], "total"),
        ]
    return pd.DataFrame(rows, columns=["line", "value", "type"])


def scenario_table(inp: CommissionInputs) -> pd.DataFrame:
    scenarios = {
        "Downside": 0.82,
        "Plan": inp.achievement,
        "High performance": 0.98,
        "Stretch": 1.04,
    }
    rows = []
    for name, achievement in scenarios.items():
        s = CommissionInputs(**{**asdict(inp), "achievement": achievement})
        r = top_down(s)
        rows.append(
            {
                "scenario": name,
                "achievement": achievement,
                "earned": r["earned"],
                "expense": r["expense"],
                "cash": r["cash"],
            }
        )
    return pd.DataFrame(rows)
