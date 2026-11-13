import pytest
from ski_resort_pass import process_resort_bookings, check_chairlift_anemometer


def test_adult_full_day_booking():
    groups = [{"is_active": True, "duration": "full_day",
               "skiers": [{"age": 30}]}]
    assert process_resort_bookings(groups, 15) == {
        "total_revenue": 80.0, "status": "COMPLETED"
    }


def test_season_child_with_gear_and_locker():
    groups = [{"is_active": True, "duration": "season",
               "includes_lodge_locker": True,
               "skiers": [{"age": 10, "gear_rental": True}]}]
    assert process_resort_bookings(groups, 20)["total_revenue"] == 235.0


def test_half_day_senior_booking():
    groups = [{"is_active": True, "duration": "half_day",
               "skiers": [{"age": 70}]}]
    assert process_resort_bookings(groups, 15)["total_revenue"] == 35.0


def test_inactive_group_is_ignored():
    assert process_resort_bookings([{"is_active": False}], 15)["status"] == "ZERO_SALES"


def test_invalid_input_raises_value_error():
    with pytest.raises(ValueError):
        process_resort_bookings("not-a-list", 15)
    with pytest.raises(ValueError):
        process_resort_bookings([], -1)


def test_invalid_duration_and_invalid_age_are_rejected():
    groups = [
        {"is_active": True, "duration": "weekly", "skiers": [{"age": 30}]},
        {"is_active": True, "duration": "full_day",
         "skiers": [{"age": 0}, {"age": -2}]},
    ]
    assert process_resort_bookings(groups, 15)["status"] == "ZERO_SALES"


def test_blackout_override_on_full_day_charges_half_rate():
    groups = [{"is_active": True, "duration": "full_day",
               "skiers": [{"age": 30, "blackout_override": True}]}]
    assert process_resort_bookings(groups, 15)["total_revenue"] == 40.0


def test_blackout_override_cancels_half_day_group():
    groups = [{"is_active": True, "duration": "half_day",
               "skiers": [{"age": 30, "blackout_override": True},
                          {"age": 30}]}]
    assert process_resort_bookings(groups, 15)["status"] == "ZERO_SALES"


def test_more_than_four_rejections_triggers_audit_review():
    groups = [{"is_active": True, "duration": "full_day",
               "skiers": [{"age": 0} for _ in range(5)]}]
    assert process_resort_bookings(groups, 15)["status"] == "AUDIT_REVIEW"


def test_no_wind_data():
    assert check_chairlift_anemometer([]) == "NO_DATA"


def test_wind_safe_and_single_gust():
    assert check_chairlift_anemometer([[45, 46, 40], [44]]) == "SAFE_OPERATION"


def test_two_consecutive_gusts_suspend_lift():
    assert check_chairlift_anemometer([[46, 47]]) == "SUSPEND_LIFT"
