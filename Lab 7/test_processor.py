import math
import pytest
from hypothesis import given, settings, strategies as st

from processor import (
    parse_season_pass_validity,
    compute_trail_gradient,
    calculate_lift_access_tier,
)


# Fuzz each public function with arbitrary Unicode strings and None.
# Exceptions are intentionally NOT caught: a crash must fail the test.
@given(st.text() | st.none())
@settings(max_examples=200)
def test_parse_season_pass_validity_does_not_crash(value):
    result = parse_season_pass_validity(value)
    assert isinstance(result, str)


@given(st.text() | st.none())
@settings(max_examples=200)
def test_compute_trail_gradient_does_not_crash(value):
    result = compute_trail_gradient(value)
    assert isinstance(result, (int, float))
    assert math.isfinite(result)


@given(st.text() | st.none())
@settings(max_examples=200)
def test_calculate_lift_access_tier_does_not_crash(value):
    result = calculate_lift_access_tier(value)
    assert isinstance(result, (int, float))
    assert math.isfinite(result)


@given(
    st.integers(min_value=2026, max_value=9999),
    st.integers(min_value=1, max_value=12),
    st.integers(min_value=1, max_value=28),
)
def test_valid_future_dates_are_accepted(year, month, day):
    result = parse_season_pass_validity(f"{year}/{month:02d}/{day:02d}")
    assert result.endswith("(VALID)")


@pytest.mark.parametrize(
    "value",
    ["", "2026-01-01", "2026/13/01", "2026/02/30", "abc/01/01", None, 123],
)
def test_invalid_dates_return_invalid_message(value):
    assert parse_season_pass_validity(value) == "Pass Expiry: INVALID"


@given(
    st.integers(min_value=1, max_value=100000),
    st.integers(min_value=1, max_value=100000),
)
def test_positive_drop_and_distance_give_nonnegative_gradient(drop, distance):
    result = compute_trail_gradient(f"{drop}:{distance}")
    assert result >= 0
    assert math.isfinite(result)


@pytest.mark.parametrize(
    "value",
    ["", "100", "100:0", "-10:100", "abc:100", "100:abc", None,
     "nan:100", "inf:2", "1e308:1e-308"],
)
def test_invalid_gradient_inputs_return_zero(value):
    assert compute_trail_gradient(value) == 0.0


@pytest.mark.parametrize(
    ("zone", "expected"),
    [
        ("BEG", 35.0),
        ("INT", 60.0),
        ("ADV", 85.0),
        ("ALL", 110.0),
        (" beg ", 35.0),
        ("int-west", 60.0),
    ],
)
def test_supported_zones_return_expected_price(zone, expected):
    assert calculate_lift_access_tier(zone) == expected


@pytest.mark.parametrize("value", [None, "", "BAD", "UNKNOWN", 123])
def test_unknown_or_invalid_zones_return_zero(value):
    assert calculate_lift_access_tier(value) == 0.0
