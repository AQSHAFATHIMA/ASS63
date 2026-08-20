from ICUAllocation import ICUAllocation


def test_critical_patient():

    icu = ICUAllocation()

    p = icu.add_patient(
        "P1",
        65,
        85,
        130,
        85,
        39.5,
        "yes",
        "no"
    )

    assert p["priority"] == "CRITICAL"

    print("Critical patient: PASS")


def test_normal_patient():

    icu = ICUAllocation()

    p = icu.add_patient(
        "P2",
        30,
        98,
        80,
        120,
        37,
        "no",
        "no"
    )

    assert p["priority"] == "LOW"

    print("Normal patient: PASS")


def test_emergency_case():

    icu = ICUAllocation()

    p = icu.add_patient(
        "P3",
        30,
        98,
        80,
        120,
        37,
        "no",
        "yes"
    )

    assert p["priority"] == "CRITICAL"

    print("Emergency case: PASS")


def test_no_icu_beds():

    icu = ICUAllocation()

    icu.add_patient(
        "P4",
        65,
        85,
        130,
        85,
        39,
        "yes",
        "no"
    )

    result = icu.allocate_beds(0)

    assert result["allocated"] == []
    assert "P4" in result["waiting"]

    print("No ICU beds: PASS")


def test_duplicate_patient():

    icu = ICUAllocation()

    icu.add_patient(
        "P5",
        40,
        98,
        80,
        120,
        37,
        "no",
        "no"
    )

    result = icu.add_patient(
        "P5",
        50,
        95,
        90,
        110,
        38,
        "no",
        "no"
    )

    assert result == "Duplicate patient ID"

    print("Duplicate patient: PASS")


def test_invalid_oxygen():

    icu = ICUAllocation()

    result = icu.add_patient(
        "P6",
        40,
        101,
        80,
        120,
        37,
        "no",
        "no"
    )

    assert result == "Invalid oxygen level"

    print("Invalid oxygen level: PASS")


def test_invalid_heart_rate():

    icu = ICUAllocation()

    result = icu.add_patient(
        "P7",
        40,
        98,
        0,
        120,
        37,
        "no",
        "no"
    )

    assert result == "Invalid heart rate"

    print("Invalid heart rate: PASS")


def test_priority_boundary():

    icu = ICUAllocation()

    # Oxygen < 90 = 40
    # Heart rate > 120 = 30
    # Total = 70 -> CRITICAL
    p = icu.add_patient(
        "P8",
        40,
        85,
        130,
        120,
        37,
        "no",
        "no"
    )

    assert p["score"] == 70
    assert p["priority"] == "CRITICAL"

    print("Priority boundary values: PASS")


def test_multiple_patients_same_bed():

    icu = ICUAllocation()

    icu.add_patient(
        "P9",
        70,
        85,
        130,
        80,
        39,
        "yes",
        "no"
    )

    icu.add_patient(
        "P10",
        50,
        92,
        110,
        90,
        38,
        "yes",
        "no"
    )

    icu.add_patient(
        "P11",
        30,
        98,
        80,
        120,
        37,
        "no",
        "no"
    )

    result = icu.allocate_beds(1)

    assert len(result["allocated"]) == 1
    assert result["allocated"][0] == "P9"

    assert len(result["waiting"]) == 2

    print(
        "Multiple patients competing "
        "for same bed: PASS"
    )


print("===== ICU ALLOCATION QA =====")

test_critical_patient()
test_normal_patient()
test_emergency_case()
test_no_icu_beds()
test_duplicate_patient()
test_invalid_oxygen()
test_invalid_heart_rate()
test_priority_boundary()
test_multiple_patients_same_bed()

print("\nALL ICU TESTS PASSED")
