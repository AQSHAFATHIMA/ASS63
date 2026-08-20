class ICUAllocation:

    def __init__(self):
        self.patients = []

    # Add patient
    def add_patient(
        self,
        patient_id,
        age,
        oxygen,
        heart_rate,
        blood_pressure,
        temperature,
        condition,
        emergency
    ):

        # Duplicate patient ID
        for patient in self.patients:
            if patient["id"] == patient_id:
                return "Duplicate patient ID"

        # Oxygen validation
        if oxygen < 0 or oxygen > 100:
            return "Invalid oxygen level"

        # Heart-rate validation
        if heart_rate <= 0:
            return "Invalid heart rate"

        if age <= 0:
            return "Invalid age"

        if blood_pressure <= 0:
            return "Invalid blood pressure"

        # Calculate priority score
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

        if condition.lower() == "yes":
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

        self.patients.append({
            "id": patient_id,
            "age": age,
            "oxygen": oxygen,
            "heart_rate": heart_rate,
            "blood_pressure": blood_pressure,
            "temperature": temperature,
            "condition": condition,
            "emergency": emergency,
            "score": score,
            "priority": priority,
            "allocated": False
        })

        return {
            "message": "Patient added",
            "score": score,
            "priority": priority
        }

    # Allocate ICU beds
    def allocate_beds(self, beds):

        if beds < 0:
            return "Invalid number of beds"

        if beds == 0:
            for patient in self.patients:
                patient["allocated"] = False

            return "No ICU beds - Waiting list"

        # Emergency cases first, then priority
        priority_order = {
            "CRITICAL": 4,
            "HIGH": 3,
            "MEDIUM": 2,
            "LOW": 1
        }

        self.patients.sort(
            key=lambda p: (
                p["emergency"].lower() == "yes",
                priority_order[p["priority"]]
            ),
            reverse=True
        )

        result = []

        for i, patient in enumerate(self.patients):

            if i < beds:

                patient["allocated"] = True

                result.append(
                    patient["id"] +
                    " -> ICU BED (" +
                    patient["priority"] +
                    ")"
                )

            else:

                patient["allocated"] = False

                result.append(
                    patient["id"] +
                    " -> WAITING LIST"
                )

        return result

    # Waiting list
    def waiting_list(self):

        return [
            p["id"]
            for p in self.patients
            if not p["allocated"]
        ]

    # Get patient
    def get_patient(self, patient_id):

        for patient in self.patients:
            if patient["id"] == patient_id:
                return patient

        return None


# ---------------- MAIN PROGRAM ----------------

icu = ICUAllocation()

print("===== ICU RESOURCE ALLOCATION =====")

patient_id = input("Patient ID: ")
age = int(input("Age: "))
oxygen = float(input("Oxygen level: "))
heart_rate = int(input("Heart rate: "))
blood_pressure = int(input("Blood pressure: "))
temperature = float(input("Temperature: "))
condition = input("Existing medical condition (yes/no): ")
emergency = input("Emergency case (yes/no): ")
beds = int(input("Available ICU beds: "))

result = icu.add_patient(
    patient_id,
    age,
    oxygen,
    heart_rate,
    blood_pressure,
    temperature,
    condition,
    emergency
)

if isinstance(result, str):

    print(result)

else:

    print("\nPriority Score:",
          result["score"])

    print("Priority:",
          result["priority"])

    allocation = icu.allocate_beds(beds)

    print("\n===== ICU ALLOCATION =====")

    if isinstance(allocation, str):

        print(allocation)

    else:

        for item in allocation:
            print(item)

        print("\nWaiting List:",
              icu.waiting_list())
