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

        self.registered = {}

    def register(
        self,
        student_id,
        program,
        semester,
        completed_courses,
        selected_courses,
        max_credits
    ):

        if student_id not in self.registered:
            self.registered[student_id] = []

        current = self.registered[student_id]

        # Check each selected course
        for course in selected_courses:

            # Invalid course
            if course not in self.courses:
                return "Invalid course"

            info = self.courses[course]

            # Semester restriction
            if semester != info["semester"]:
                return "Semester restriction"

            # Duplicate registration
            if course in current:
                return "Duplicate registration"

            # Prerequisite
            if info["prerequisite"] not in completed_courses:
                return "Missing prerequisite"

            # Course capacity
            if info["capacity"] <= 0:
                return "Course is full"

        # Calculate credits
        total = sum(
            self.courses[c]["credits"]
            for c in current
        )

        for course in selected_courses:
            total += self.courses[course]["credits"]

        # Credit limit
        if total > max_credits:
            return "Credit limit exceeded"

        # Timetable clash
        times = [
            self.courses[c]["time"]
            for c in current
        ]

        for course in selected_courses:

            if self.courses[course]["time"] in times:
                return "Timetable conflict"

            times.append(
                self.courses[course]["time"]
            )

        # Register courses
        for course in selected_courses:

            current.append(course)

            self.courses[course]["capacity"] -= 1

        return {
            "status": "Registration successful",
            "courses": current,
            "total_credits": total
        }

    def total_credits(self, student_id):

        if student_id not in self.registered:
            return 0

        return sum(
            self.courses[c]["credits"]
            for c in self.registered[student_id]
        )


# Jenkins-friendly demonstration
if __name__ == "__main__":

    system = CourseRegistration()

    result = system.register(
        "S101",
        "CSE",
        2,
        ["Programming", "Data Structures"],
        ["DBMS"],
        8
    )

    print(result)
