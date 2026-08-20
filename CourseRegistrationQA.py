from CourseRegistration import CourseRegistration


def test_valid_registration():

    system = CourseRegistration()

    result = system.register(
        "S1",
        "CSE",
        2,
        ["Programming"],
        ["DBMS"],
        8
    )

    assert result["status"] == \
        "Registration successful"

    assert system.total_credits("S1") == 4

    print("Valid registration: PASS")


def test_missing_prerequisite():

    system = CourseRegistration()

    result = system.register(
        "S2",
        "CSE",
        2,
        [],
        ["DBMS"],
        8
    )

    assert "Missing prerequisite" in result

    print("Missing prerequisite: PASS")


def test_credit_limit():

    system = CourseRegistration()

    result = system.register(
        "S3",
        "CSE",
        2,
        ["Programming", "Data Structures"],
        ["DBMS", "AI"],
        7
    )

    assert result == "Credit limit exceeded"

    print("Credit-limit violation: PASS")


def test_timetable_conflict():

    system = CourseRegistration()

    # DBMS = 9-10
    system.register(
        "S4",
        "CSE",
        2,
        ["Programming"],
        ["DBMS"],
        8
    )

    # ML also uses 9-10,
    # but ML belongs to semester 3.
    # Test conflict separately by
    # modifying semester for this test.
    system.courses["ML"]["semester"] = 2

    result = system.register(
        "S4",
        "CSE",
        2,
        ["Statistics"],
        ["ML"],
        8
    )

    assert "Timetable conflict" in result

    print("Timetable conflict: PASS")


def test_full_course():

    system = CourseRegistration()

    system.courses["DBMS"]["capacity"] = 0

    result = system.register(
        "S5",
        "CSE",
        2,
        ["Programming"],
        ["DBMS"],
        8
    )

    assert "Course is full" in result

    print("Full course: PASS")


def test_duplicate_registration():

    system = CourseRegistration()

    system.register(
        "S6",
        "CSE",
        2,
        ["Programming"],
        ["DBMS"],
        8
    )

    result = system.register(
        "S6",
        "CSE",
        2,
        ["Programming"],
        ["DBMS"],
        8
    )

    assert "Duplicate registration" in result

    print("Duplicate registration: PASS")


def test_invalid_course():

    system = CourseRegistration()

    result = system.register(
        "S7",
        "CSE",
        2,
        ["Programming"],
        ["Java"],
        8
    )

    assert "Invalid course" in result

    print("Invalid course: PASS")


def test_semester_restriction():

    system = CourseRegistration()

    result = system.register(
        "S8",
        "CSE",
        1,
        ["Programming"],
        ["DBMS"],
        8
    )

    assert "Semester restriction" in result

    print("Semester restriction: PASS")


def test_boundary_credit():

    system = CourseRegistration()

    result = system.register(
        "S9",
        "CSE",
        2,
        ["Programming", "Data Structures"],
        ["DBMS", "AI"],
        8
    )

    assert result["total_credits"] == 8

    print("Boundary credit values: PASS")


# ---------------- RUN ALL TESTS ----------------

print("===== COURSE REGISTRATION QA =====")

test_valid_registration()
test_missing_prerequisite()
test_credit_limit()
test_timetable_conflict()
test_full_course()
test_duplicate_registration()
test_invalid_course()
test_semester_restriction()
test_boundary_credit()

print("\nALL COURSE REGISTRATION TESTS PASSED")
