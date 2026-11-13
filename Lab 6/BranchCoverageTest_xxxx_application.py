import pytest
from ski_resort_pass import process_resort_bookings, check_chairlift_anemometer


def test_invalid_groups_type_branch():
    with pytest.raises(ValueError):
        process_resort_bookings(None, 10)


def test_negative_facility_fee_branch():
    with pytest.raises(ValueError):
        process_resort_bookings([], -0.01)


def test_inactive_group_branch():
    assert process_resort_bookings([{"is_active": False}], 10)["status"] == "ZERO_SALES"


@pytest.mark.parametrize(("duration", "age", "expected"), [
    ("season", 30, 300.0),
    ("full_day", 30, 80.0),
    ("half_day", 30, 50.0),
])
def test_each_valid_pass_duration(duration, age, expected):
    groups = [{"is_active": True, "duration": duration,
               "skiers": [{"age": age}]}]
    assert process_resort_bookings(groups, 10)["total_revenue"] == expected


def test_invalid_duration_branch():
    groups = [{"is_active": True, "duration": "weekend",
               "skiers": [{"age": 30}]}]
    assert process_resort_bookings(groups, 10)["status"] == "ZERO_SALES"


def test_invalid_age_branch_and_rejection_threshold_not_exceeded():
    groups = [{"is_active": True, "duration": "full_day",
               "skiers": [{"age": 0}]}]
    assert process_resort_bookings(groups, 10)["status"] == "ZERO_SALES"


def test_child_discount_branch():
    groups = [{"is_active": True, "duration": "full_day",
               "skiers": [{"age": 11}]}]
    assert process_resort_bookings(groups, 10)["total_revenue"] == 48.0


def test_senior_discount_branch():
    groups = [{"is_active": True, "duration": "full_day",
               "skiers": [{"age": 65}]}]
    assert process_resort_bookings(groups, 10)["total_revenue"] == 56.0


def test_regular_adult_branch_and_gear_rental_true():
    groups = [{"is_active": True, "duration": "full_day",
               "skiers": [{"age": 30, "gear_rental": True}]}]
    assert process_resort_bookings(groups, 10)["total_revenue"] == 115.0


def test_gear_rental_false_branch():
    groups = [{"is_active": True, "duration": "full_day",
               "skiers": [{"age": 30, "gear_rental": False}]}]
    assert process_resort_bookings(groups, 10)["total_revenue"] == 80.0


def test_blackout_override_non_half_day_branch():
    groups = [{"is_active": True, "duration": "season",
               "skiers": [{"age": 30, "blackout_override": True}]}]
    assert process_resort_bookings(groups, 10)["total_revenue"] == 150.0


def test_blackout_override_half_day_break_branch():
    groups = [{"is_active": True, "duration": "half_day",
               "skiers": [{"age": 30, "blackout_override": True}]}]
    assert process_resort_bookings(groups, 10)["status"] == "ZERO_SALES"


def test_locker_fee_true_and_false_branches():
    with_locker = [{"is_active": True, "duration": "full_day",
                    "includes_lodge_locker": True, "skiers": [{"age": 30}]}]
    without_locker = [{"is_active": True, "duration": "full_day",
                       "includes_lodge_locker": False, "skiers": [{"age": 30}]}]
    assert process_resort_bookings(with_locker, 10)["total_revenue"] == 90.0
    assert process_resort_bookings(without_locker, 10)["total_revenue"] == 80.0


def test_audit_review_branch_after_more_than_four_rejections():
    groups = [{"is_active": True, "duration": "full_day",
               "skiers": [{"age": 0} for _ in range(5)]}]
    assert process_resort_bookings(groups, 10)["status"] == "AUDIT_REVIEW"


def test_completed_status_branch():
    groups = [{"is_active": True, "duration": "full_day",
               "skiers": [{"age": 30}]}]
    assert process_resort_bookings(groups, 10)["status"] == "COMPLETED"


def test_zero_sales_status_branch():
    assert process_resort_bookings([], 10)["status"] == "ZERO_SALES"


def test_anemometer_no_data_branch():
    assert check_chairlift_anemometer([]) == "NO_DATA"


def test_wind_at_threshold_is_not_a_gust():
    assert check_chairlift_anemometer([[45]]) == "SAFE_OPERATION"


def test_single_gust_does_not_suspend():
    assert check_chairlift_anemometer([[46]]) == "SAFE_OPERATION"


def test_safe_reading_resets_gust_streak():
    assert check_chairlift_anemometer([[46, 45, 47]]) == "SAFE_OPERATION"


def test_two_consecutive_gusts_suspend():
    assert check_chairlift_anemometer([[46, 47]]) == "SUSPEND_LIFT"


def test_gusts_on_later_lift_stream_suspend():
    assert check_chairlift_anemometer([[46], [47, 48]]) == "SUSPEND_LIFT"
