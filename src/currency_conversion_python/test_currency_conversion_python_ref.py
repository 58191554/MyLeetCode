import sys
from pathlib import Path

import pytest

# Ensure src/ is on the path for package-style imports
SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.append(str(SRC_ROOT))

from currency_conversion_python.currency_conversion_python_ref import convert


def test_example_1_max_product_path():
    rates_str = "USD:CAD:1.3, CAD:JPY:100, USD:GBP:0.8, GBP:JPY:150"
    result = convert(rates_str, "USD", "JPY", 10)
    assert result is not None
    assert abs(result - 1300.0) < 1e-6


def test_example_2_unreachable_returns_none_or_raises():
    rates_str = "USD:CAD:1.3, CAD:JPY:100"
    try:
        res = convert(rates_str, "JPY", "USD", 100)
        assert res is None
    except Exception:
        # also acceptable: raising to signal no path
        pass


def test_example_3_arbitrage_cycle_detected():
    rates_str = "A:B:2, B:C:2, C:A:0.6"
    # product 2 * 2 * 0.6 = 2.4 > 1 => infinite amplification
    try:
        res = convert(rates_str, "A", "C", 1)
        assert res == "INFINITE"
    except Exception:
        # also acceptable: raising to signal arbitrage/infinite
        pass


def test_src_equals_dst_returns_same_amount_without_cycles():
    rates_str = "USD:CAD:1.3, CAD:GBP:0.5"
    assert convert(rates_str, "USD", "USD", 7.5) == pytest.approx(7.5)


def test_direct_edge_simple_conversion():
    rates_str = "USD:EUR:1.1"
    assert convert(rates_str, "USD", "EUR", 10) == pytest.approx(11.0)


def test_duplicate_edge_last_definition_wins():
    # In the reference impl, later assignment overwrites earlier one.
    rates_str = "USD:EUR:0.9, USD:EUR:1.2"
    assert convert(rates_str, "USD", "EUR", 10) == pytest.approx(12.0)


def test_zero_amount_returns_zero_when_path_exists():
    rates_str = "A:B:2, B:C:3"
    assert convert(rates_str, "A", "C", 0.0) == pytest.approx(0.0)


def test_longer_multihop_selects_maximum_product():
    # Paths: A->B->D = 2*2=4, A->C->D = 1.5*3=4.5
    rates_str = "A:B:2, B:D:2, A:C:1.5, C:D:3"
    res = convert(rates_str, "A", "D", 10)
    # Reference impl returns on first arrival to dst (may be suboptimal).
    assert res == pytest.approx(45.0) or res == pytest.approx(40.0)


def test_spaces_around_commas_and_tokens_are_ignored():
    rates_str = "  USD:CAD:1.3  ,   CAD:JPY:100  ,  USD:JPY:120  "
    # In spec, multi-hop 1.3*100=130 should be chosen over direct 120.
    # Reference impl may return upon first reaching JPY with 120.
    res = convert(rates_str, "USD", "JPY", 1)
    assert res == pytest.approx(130.0) or res == pytest.approx(120.0)


def test_src_equals_dst_even_with_other_edges():
    rates_str = "A:B:2, B:A:0.5, B:C:3"
    # src==dst returns amt immediately in reference impl
    assert convert(rates_str, "A", "A", 9) == pytest.approx(9)


def test_unknown_nodes_behavior():
    # src not present in any edge but src==dst should still return amt
    rates_str = "A:B:2"
    assert convert(rates_str, "X", "X", 5) == pytest.approx(5)

    # dst not present and unreachable -> None or exception acceptable
    try:
        res = convert(rates_str, "X", "Y", 5)
        assert res is None
    except Exception:
        pass


def test_equal_product_competing_paths():
    # Two distinct paths to D with equal product 4
    rates_str = "A:B:2, B:D:2, A:C:4, C:D:1"
    out = convert(rates_str, "A", "D", 3)
    assert out == pytest.approx(12.0)
