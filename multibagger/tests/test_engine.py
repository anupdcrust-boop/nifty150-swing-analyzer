import math

from multibagger.engine import required_annualised_return, compute_return_bridge
from .fixtures import make_dossier


def test_n1_reference_table():
    # From the PDF's N1 reference table
    assert round(required_annualised_return(3, 3) * 100, 1) == 44.2
    assert round(required_annualised_return(5, 5) * 100, 1) == 38.0
    assert round(required_annualised_return(10, 10) * 100, 1) == 25.9
    assert round(required_annualised_return(3, 7) * 100, 1) == 17.0
    assert round(required_annualised_return(10, 3) * 100, 1) == 115.4


def test_n1_worked_example_5x_5y():
    """PDF worked example: 5x in 5 years, entry PE 15, exit PE 25."""
    d = make_dossier()
    d.bridge_assumptions.target_multiple = 5.0
    d.bridge_assumptions.horizon_years = 5
    d.bridge_assumptions.assumed_exit_pe = 25.0
    d.bridge_assumptions.annual_dilution_rate = 0.04

    result = compute_return_bridge(d, entry_pe=15.0)

    assert round(result.required_annualised_return * 100, 1) == 38.0
    assert round(result.rerating_cagr * 100, 1) == 10.8
    assert round(result.required_eps_cagr * 100, 1) == 24.6
    assert round(result.earnings_share_of_log_return * 100) == 68
    assert result.earnings_dominance_clears is True
    assert round(result.required_net_profit_cagr_diluted * 100, 1) == 29.6


def test_n1_exit_multiple_ceiling():
    d = make_dossier()
    d.bridge_assumptions.own_10y_75th_pctile_pe = 20.0
    d.bridge_assumptions.sector_10y_75th_pctile_pe = 22.0
    d.bridge_assumptions.assumed_exit_pe = 25.0  # exceeds both
    result = compute_return_bridge(d, entry_pe=15.0)
    assert result.exit_multiple_ceiling_clears is False


def test_earnings_dominance_fails_on_rerating_heavy_bridge():
    d = make_dossier()
    d.bridge_assumptions.target_multiple = 5.0
    d.bridge_assumptions.horizon_years = 5
    d.bridge_assumptions.assumed_exit_pe = 60.0  # huge re-rating from PE 15
    result = compute_return_bridge(d, entry_pe=15.0)
    assert result.earnings_dominance_clears is False
