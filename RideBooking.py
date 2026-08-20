class RideBooking:

    VEHICLES = {
        "Bike": {
            "base": 30,
            "per_km": 10,
            "max_passengers": 1
        },
        "Sedan": {
            "base": 60,
            "per_km": 15,
            "max_passengers": 4
        },
        "SUV": {
            "base": 100,
            "per_km": 20,
            "max_passengers": 6
        },
        "Premium": {
            "base": 150,
            "per_km": 30,
            "max_passengers": 4
        }
    }

    MAX_DISCOUNT = 20

    def __init__(self):
        self.drivers = {
            "Bike": ["D101"],
            "Sedan": ["D201"],
            "SUV": ["D301"],
            "Premium": ["D401"]
        }

    # Validate booking
    def validate_booking(
            self,
            distance,
            passengers,
            vehicle,
            booking_time):

        if distance <= 0:
            return "Invalid distance"

        if vehicle not in self.VEHICLES:
            return "Unavailable vehicle"

        if passengers <= 0:
            return "Invalid passenger count"

        max_passengers = \
            self.VEHICLES[vehicle]["max_passengers"]

        if passengers > max_passengers:
            return "Excessive passengers"

        if booking_time < 0 or booking_time > 23:
            return "Invalid booking time"

        return "Valid"

    # Base fare
    def base_fare(self, vehicle):
        return self.VEHICLES[vehicle]["base"]

    # Distance fare
    def distance_fare(self, vehicle, distance):
        return self.VEHICLES[vehicle]["per_km"] * distance

    # Peak-hour surcharge
    def peak_surcharge(self, fare, booking_time):

        if 7 <= booking_time <= 10 or \
           17 <= booking_time <= 20:

            return fare * 0.20

        return 0

    # Night surcharge
    def night_surcharge(self, fare, booking_time):

        if booking_time >= 22 or booking_time < 6:
            return fare * 0.10

        return 0

    # Passenger surcharge
    def passenger_surcharge(
            self,
            passengers):

        if passengers > 2:
            return (passengers - 2) * 20

        return 0

    # Promotional discount
    def promotional_discount(self, fare):

        discount = fare * 0.10

        if discount > self.MAX_DISCOUNT:
            discount = self.MAX_DISCOUNT

        return discount

    # Driver assignment
    def assign_driver(self, vehicle):

        if vehicle not in self.drivers:
            return None

        if len(self.drivers[vehicle]) == 0:
            return None

        return self.drivers[vehicle][0]

    # Complete fare calculation
    def calculate_fare(
            self,
            distance,
            passengers,
            vehicle,
            booking_time):

        validation = self.validate_booking(
            distance,
            passengers,
            vehicle,
            booking_time
        )

        if validation != "Valid":
            return validation

        base = self.base_fare(vehicle)

        distance_cost = self.distance_fare(
            vehicle,
            distance
        )

        fare = base + distance_cost

        peak = self.peak_surcharge(
            fare,
            booking_time
        )

        night = self.night_surcharge(
            fare,
            booking_time
        )

        passenger = self.passenger_surcharge(
            passengers
        )

        before_discount = \
            fare + peak + night + passenger

        discount = self.promotional_discount(
            before_discount
        )

        final_fare = \
            before_discount - discount

        driver = self.assign_driver(vehicle)

        if driver is None:
            return "Driver unavailable"

        return {
            "base_fare": base,
            "distance_fare": distance_cost,
            "peak_surcharge": peak,
            "night_surcharge": night,
            "passenger_surcharge": passenger,
            "promotional_discount": discount,
            "final_fare": final_fare,
            "driver": driver
        }


# ---------------- MAIN PROGRAM ----------------

ride = RideBooking()

print("===== RIDE BOOKING =====")

customer = input("Customer ID: ")
pickup = input("Pickup location: ")
drop = input("Drop location: ")

distance = float(input("Distance (km): "))
passengers = int(input("Number of passengers: "))

print("\nVehicle Types:")
print("Bike")
print("Sedan")
print("SUV")
print("Premium")

vehicle = input("Vehicle type: ")

booking_time = int(
    input("Booking time (0-23): ")
)

result = ride.calculate_fare(
    distance,
    passengers,
    vehicle,
    booking_time
)

if isinstance(result, str):

    print("\nBooking rejected:", result)

else:

    print("\n===== RIDE DETAILS =====")

    print("Customer ID:", customer)
    print("Pickup:", pickup)
    print("Drop:", drop)
    print("Vehicle:", vehicle)

    print("Base fare:",
          result["base_fare"])

    print("Distance fare:",
          result["distance_fare"])

    print("Peak surcharge:",
          result["peak_surcharge"])

    print("Night surcharge:",
          result["night_surcharge"])

    print("Passenger surcharge:",
          result["passenger_surcharge"])

    print("Promotional discount:",
          result["promotional_discount"])

    print("Final fare:",
          round(result["final_fare"], 2))

    print("Driver assigned:",
          result["driver"])
