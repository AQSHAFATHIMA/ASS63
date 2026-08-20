from ICUAllocation import ICUAllocation


def test_critical_patient():

    icu = ICUAllocation()

    result = icu.add_patient(
        "P1",
        65,
        85,
        130,
        85,
        39.5,
        "yes",
        "no"
    )

    assert result["priority"] == "CRITICAL"

    print("Critical patient: PASS")


def test_normal_patient():

    icu = ICUAllocation()

    result = icu.add_patient(
        "P2",
        30,
        98,
        75,
        120,
        37,
        "no",
        "no"
    )

    assert result["priority"] == "LOW"

    print("Normal patient: PASS")


def test_emergency_case():

    icu = ICUAllocation()

    result = icu.add_patient(
        "P3",
        25,
        98,
        80,
        120,
        37,
        "no",
        "yes"
    )

    assert result["priority"] == "CRITICAL"

    print("Emergency case: PASS")


def test_no_icu_beds():

    icu = ICUAllocation()

    icu.add_patient(
        "P4",
        60,
        85,
        130,
        80,
        39,
        "yes",
        "no"
    )

    result = icu.allocate_beds(0)

    assert result == \
        "No ICU beds - Waiting list"

    assert "P4" in icu.waiting_list()

    print("No ICU beds: PASS")


def test_duplicate_patient():

    icu = ICUAllocation()

    icu.add_patient(
        "P5",
        40,
        95,
        80,
        120,
        37,
        "no",
        "no"
    )

    result = icu.add_patient(
        "P5",
        50,
        90,
        100,
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
        105,
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
        -10,
        120,
        37,
        "no",
        "no"
    )

    assert result == "Invalid heart rate"

    print("Invalid heart rate: PASS")


def test_priority_boundaries():

    icu = ICUAllocation()

    # Score exactly 60
    result = icu.add_patient(
        "P8",
        40,
        85,
        120,
        90,
        37,
        "no",
        "no"
    )

    assert result["priority"] == "CRITICAL"

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

    assert "P9 -> ICU BED" in result

    assert "P10" in icu.waiting_list()
    assert "P11" in icu.waiting_list()

    print(
        "Multiple patients competing "
        "for same bed: PASS"
    )


# ---------------- RUN ALL TESTS ----------------

print("===== ICU ALLOCATION QA =====")

test_critical_patient()
test_normal_patient()
test_emergency_case()
test_no_icu_beds()
test_duplicate_patient()
test_invalid_oxygen()
test_invalid_heart_rate()
test_priority_boundaries()
test_multiple_patients_same_bed()

print("\nALL ICU TESTS PASSED")
