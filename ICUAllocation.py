class ICUAllocation:

    def __init__(self):
        self.patients = []

    def add_patient(
        self,
        patient_id,
        age,
        oxygen,
        heart_rate,
        blood_pressure,
        temperature,
        medical_condition,
        emergency
    ):

        # Duplicate patient ID
        for p in self.patients:
            if p["id"] == patient_id:
                return "Duplicate patient ID"

        # Validation
        if age <= 0:
            return "Invalid age"

        if oxygen < 0 or oxygen > 100:
            return "Invalid oxygen level"

        if heart_rate <= 0:
            return "Invalid heart rate"

        if blood_pressure <= 0:
            return "Invalid blood pressure"

        # Priority score
        score = 0

        if oxygen < 90:
            score += 40
        elif oxygen < 95:
            score += 20

        if heart_rate > 120:
            score += 30
        elif heart_rate > 100:
            score += 15

        if blood_pressure < 90:
            score += 20

        if temperature > 39:
            score += 10

        if medical_condition.lower() == "yes":
            score += 10

        # Emergency override
        if emergency.lower() == "yes":
            priority = "CRITICAL"
        elif score >= 60:
            priority = "CRITICAL"
        elif score >= 40:
            priority = "HIGH"
        elif score >= 20:
            priority = "MEDIUM"
        else:
            priority = "LOW"

        patient = {
            "id": patient_id,
            "age": age,
            "oxygen": oxygen,
            "heart_rate": heart_rate,
            "blood_pressure": blood_pressure,
            "temperature": temperature,
            "condition": medical_condition,
            "emergency": emergency,
            "score": score,
            "priority": priority,
            "bed": False
        }

        self.patients.append(patient)

        return patient

    def allocate_beds(self, beds):

        if beds < 0:
            return "Invalid bed count"

        if beds == 0:
            return {
                "allocated": [],
                "waiting": [
                    p["id"] for p in self.patients
                ]
            }

        priority_value = {
            "CRITICAL": 4,
            "HIGH": 3,
            "MEDIUM": 2,
            "LOW": 1
        }

        # Emergency patients first,
        # then priority
        self.patients.sort(
            key=lambda p: (
                p["emergency"].lower() == "yes",
                priority_value[p["priority"]]
            ),
            reverse=True
        )

        allocated = []
        waiting = []

        for i, patient in enumerate(self.patients):

            if i < beds:
                patient["bed"] = True
                allocated.append(patient["id"])

            else:
                patient["bed"] = False
                waiting.append(patient["id"])

        return {
            "allocated": allocated,
            "waiting": waiting
        }


# No input() — Jenkins-friendly demonstration
if __name__ == "__main__":

    icu = ICUAllocation()

    patient = icu.add_patient(
        "P101",
        65,
        85,
        130,
        85,
        39.5,
        "yes",
        "no"
    )

    print("Patient:", patient["id"])
    print("Priority score:", patient["score"])
    print("Priority:", patient["priority"])

    result = icu.allocate_beds(1)

    print("Allocated:", result["allocated"])
    print("Waiting:", result["waiting"])
