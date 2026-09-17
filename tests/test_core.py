from core import CommissionInputs, top_down, bottom_up, payline


def test_top_down_ties():
    r = top_down(CommissionInputs())
    assert r["total_variable_potential"] > 0
    assert round(r["earned"], 2) == round(r["total_variable_potential"] * 0.90, 2)
    assert round(r["expense"], 2) == round(r["current_year_expense"] + r["prior_amortization"], 2)


def test_bottom_up_components_sum():
    r = bottom_up(CommissionInputs())
    expected = r["revenue_component"] + r["services_component"] + r["early_renewal_bonus"] + r["net_accelerators"]
    assert round(r["earned"], 2) == round(expected, 2)


def test_accelerator_is_nonlinear_above_quota():
    assert payline(1.20) > 1.20
    assert payline(1.00) == 1.00
