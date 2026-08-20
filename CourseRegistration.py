class CourseRegistration:

    def __init__(self):
        self.courses = {
            "DBMS": {
                "credits": 4,
                "prerequisite": "Programming",
                "capacity": 2,
                "semester": 2,
                "time": "9-10"
            },

            "AI": {
                "credits": 4,
                "prerequisite": "Data Structures",
                "capacity": 2,
                "semester": 2,
                "time": "10-11"
            },

            "ML": {
                "credits": 3,
                "prerequisite": "Statistics",
                "capacity": 2,
                "semester": 3,
                "time": "9-10"
            },

            "Cloud": {
                "credits": 3,
                "prerequisite": "Networking",
                "capacity": 2,
                "semester": 3,
                "time": "11-12"
            }
        }

        self.registrations = {}

    # Register student
    def register(
        self,
        student_id,
        program,
        semester,
        completed_courses,
        selected_courses,
        max_credits
    ):

        if student_id not in self.registrations:
            self.registrations[student_id] = []

        registered = self.registrations[student_id]

        # Check every selected course
        for course in selected_courses:

            # Invalid course
            if course not in self.courses:
                return "Invalid course: " + course

            info = self.courses[course]

            # Semester restriction
            if semester != info["semester"]:
                return "Semester restriction: " + course

            # Duplicate registration
            if course in registered:
                return "Duplicate registration: " + course

            # Prerequisite verification
            if info["prerequisite"] not in completed_courses:
                return (
                    "Missing prerequisite for " +
                    course
                )

            # Course capacity
            if info["capacity"] <= 0:
                return "Course is full: " + course

        # Calculate selected credits
        selected_credits = 0

        for course in selected_courses:
            selected_credits += \
                self.courses[course]["credits"]

        # Existing credits
        existing_credits = 0

        for course in registered:
            existing_credits += \
                self.courses[course]["credits"]

        total_credits = \
            existing_credits + selected_credits

        # Credit limit
        if total_credits > max_credits:
            return "Credit limit exceeded"

        # Timetable conflict
        times = []

        for course in registered:
            times.append(
                self.courses[course]["time"]
            )

        for course in selected_courses:

            if self.courses[course]["time"] in times:
                return (
                    "Timetable conflict: " +
                    course
                )

            times.append(
                self.courses[course]["time"]
            )

        # Registration successful
        for course in selected_courses:

            registered.append(course)

            self.courses[course]["capacity"] -= 1

        return {
            "status": "Registration successful",
            "courses": registered,
            "total_credits": total_credits
        }

    # Get total registered credits
    def total_credits(self, student_id):

        if student_id not in self.registrations:
            return 0

        total = 0

        for course in self.registrations[student_id]:
            total += self.courses[course]["credits"]

        return total


# ---------------- MAIN PROGRAM ----------------

system = CourseRegistration()

print("===== UNIVERSITY COURSE REGISTRATION =====")

student_id = input("Student ID: ")
program = input("Program: ")
semester = int(input("Semester: "))

completed = input(
    "Completed courses (space separated): "
).split()

selected = input(
    "Courses to register (space separated): "
).split()

max_credits = int(
    input("Maximum credit limit: ")
)

result = system.register(
    student_id,
    program,
    semester,
    completed,
    selected,
    max_credits
)

print()

if isinstance(result, str):

    print("Registration failed:")
    print(result)

else:

    print(result["status"])

    print("Registered courses:",
          result["courses"])

    print("Total registered credits:",
          result["total_credits"])
