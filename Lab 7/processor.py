from datetime import date
import math


def parse_season_pass_validity(date_str):
    """Validate YYYY/MM/DD and return a normalized expiry message."""
    if not isinstance(date_str, str):
        return "Pass Expiry: INVALID"

    parts = date_str.strip().split("/")
    if len(parts) != 3 or not all(part.isdigit() for part in parts):
        return "Pass Expiry: INVALID"

    try:
        year, month, day = map(int, parts)
        parsed_date = date(year, month, day)
    except (ValueError, TypeError, OverflowError):
        return "Pass Expiry: INVALID"

    status = "VALID" if parsed_date.year >= 2026 else "EXPIRED"
    return (
        f"Pass Expiry: {parsed_date.year:04d}-"
        f"{parsed_date.month:02d}-{parsed_date.day:02d} ({status})"
    )


def compute_trail_gradient(elevation_str):
    """Calculate gradient percentage from 'vertical_drop:horizontal_distance'."""
    if not isinstance(elevation_str, str):
        return 0.0

    parts = elevation_str.strip().split(":")
    if len(parts) != 2:
        return 0.0

    try:
        drop = float(parts[0].strip())
        distance = float(parts[1].strip())
    except (ValueError, TypeError, OverflowError):
        return 0.0

    if not (math.isfinite(drop) and math.isfinite(distance)):
        return 0.0
    if drop < 0 or distance <= 0:
        return 0.0

    gradient = (drop / distance) * 100.0
    if not math.isfinite(gradient):
        return 0.0
    return round(gradient, 2)


def calculate_lift_access_tier(zone_code):
    """Return the access price for a known zone; unknown inputs return 0.0."""
    if not isinstance(zone_code, str):
        return 0.0

    prefix = zone_code.strip().upper()[:3]
    zone_rates = {
        "BEG": 35.0,
        "INT": 60.0,
        "ADV": 85.0,
        "ALL": 110.0,
    }
    return zone_rates.get(prefix, 0.0)


def main():
    print("==== Running parse_season_pass_validity ====")
    date_input = input("Enter pass expiry (YYYY/MM/DD): ")
    print(parse_season_pass_validity(date_input))

    print("\n==== Running compute_trail_gradient ====")
    elevation_input = input("Enter drop:distance (e.g. 250:1000): ")
    print("Gradient %:", compute_trail_gradient(elevation_input))

    print("\n==== Running calculate_lift_access_tier ====")
    zone_input = input("Enter zone code (e.g. BEG, INT, ALL): ")
    print("Lift Pass Price: $", calculate_lift_access_tier(zone_input))


if __name__ == "__main__":
    main()
