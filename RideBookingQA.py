from RideBooking import RideBooking


def test_normal_booking():

    r = RideBooking()

    result = r.calculate_fare(
        10, 2, "Sedan", 12
    )

    assert isinstance(result, dict)

    print("Normal booking: PASS")


def test_peak_hour():

    r = RideBooking()

    result = r.calculate_fare(
        10, 2, "Sedan", 8
    )

    assert result["peak_surcharge"] > 0

    print("Peak-hour booking: PASS")


def test_night_booking():

    r = RideBooking()

    result = r.calculate_fare(
        10, 2, "Sedan", 23
    )

    assert result["night_surcharge"] > 0

    print("Night booking: PASS")


def test_invalid_distance():

    r = RideBooking()

    result = r.calculate_fare(
        0, 2, "Sedan", 12
    )

    assert result == "Invalid distance"

    print("Invalid distance: PASS")


def test_invalid_passenger_count():

    r = RideBooking()

    result = r.calculate_fare(
        10, 0, "Sedan", 12
    )

    assert result == "Invalid passenger count"

    print("Invalid passenger count: PASS")


def test_excessive_passengers():

    r = RideBooking()

    result = r.calculate_fare(
        10, 5, "Sedan", 12
    )

    assert result == "Excessive passengers"

    print("Excessive passengers: PASS")


def test_unavailable_vehicle():

    r = RideBooking()

    result = r.calculate_fare(
        10, 2, "Auto", 12
    )

    assert result == "Unavailable vehicle"

    print("Unavailable vehicle: PASS")


def test_unavailable_driver():

    r = RideBooking()

    r.drivers["Sedan"] = []

    result = r.calculate_fare(
        10, 2, "Sedan", 12
    )

    assert result == "Driver unavailable"

    print("Unavailable driver: PASS")


def test_maximum_discount():

    r = RideBooking()

    discount = r.promotional_discount(1000)

    assert discount == r.MAX_DISCOUNT

    print("Maximum discount: PASS")


def test_multiple_vehicle_types():

    r = RideBooking()

    for vehicle in [
        "Bike",
        "Sedan",
        "SUV",
        "Premium"
    ]:

        result = r.calculate_fare(
            10,
            1,
            vehicle,
            12
        )

        assert isinstance(result, dict)

    print("Multiple vehicle types: PASS")


def test_boundary_fare():

    r = RideBooking()

    result = r.calculate_fare(
        1,
        1,
        "Bike",
        12
    )

    assert result["final_fare"] > 0

    print("Boundary fare values: PASS")


def test_driver_allocation():

    r = RideBooking()

    result = r.assign_driver("Sedan")

    assert result == "D201"

    print("Driver allocation logic: PASS")


def test_invalid_booking_time():

    r = RideBooking()

    result = r.calculate_fare(
        10,
        2,
        "Sedan",
        25
    )

    assert result == "Invalid booking time"

    print("Invalid booking time: PASS")


# ---------------- RUN ALL TESTS ----------------

print("===== RIDE BOOKING QA =====")

test_normal_booking()
test_peak_hour()
test_night_booking()
test_invalid_distance()
test_invalid_passenger_count()
test_excessive_passengers()
test_unavailable_vehicle()
test_unavailable_driver()
test_maximum_discount()
test_multiple_vehicle_types()
test_boundary_fare()
test_driver_allocation()
test_invalid_booking_time()

print("\nALL RIDE BOOKING TESTS PASSED")
