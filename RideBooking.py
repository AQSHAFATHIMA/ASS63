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

    DISCOUNT_RATE = 0.10
    MAX_DISCOUNT = 20

    def __init__(self):
        self.drivers = {
            "Bike": ["D101"],
            "Sedan": ["D201"],
            "SUV": ["D301"],
            "Premium": ["D401"]
        }

    def validate(self, distance, passengers,
                 vehicle, booking_time):

        if distance <= 0:
            return "Invalid distance"

        if vehicle not in self.VEHICLES:
            return "Unavailable vehicle"

        if passengers <= 0:
            return "Invalid passenger count"

        if passengers > self.VEHICLES[vehicle]["max_passengers"]:
            return "Excessive passengers"

        if booking_time < 0 or booking_time > 23:
            return "Invalid booking time"

        return "Valid"

    def calculate(self, customer_id, pickup, drop,
                  distance, passengers, vehicle,
                  booking_time, driver_available=True):

        result = self.validate(
            distance,
            passengers,
            vehicle,
            booking_time
        )

        if result != "Valid":
            return result

        if not driver_available:
            return "Driver unavailable"

        base = self.VEHICLES[vehicle]["base"]

        distance_fare = (
            self.VEHICLES[vehicle]["per_km"]
            * distance
        )

        fare = base + distance_fare

        # Peak hour: 7-10 and 17-20
        if 7 <= booking_time <= 10 or \
           17 <= booking_time <= 20:
            peak = fare * 0.20
        else:
            peak = 0

        # Night: 22-23 and 0-5
        if booking_time >= 22 or booking_time < 6:
            night = fare * 0.10
        else:
            night = 0

        # Passenger surcharge
        if passengers > 2:
            passenger = (passengers - 2) * 20
        else:
            passenger = 0

        total = fare + peak + night + passenger

        discount = total * self.DISCOUNT_RATE

        if discount > self.MAX_DISCOUNT:
            discount = self.MAX_DISCOUNT

        final_fare = total - discount

        driver = self.drivers[vehicle][0]

        return {
            "customer_id": customer_id,
            "pickup": pickup,
            "drop": drop,
            "base_fare": base,
            "distance_fare": distance_fare,
            "peak_surcharge": peak,
            "night_surcharge": night,
            "passenger_surcharge": passenger,
            "promotional_discount": discount,
            "final_fare": final_fare,
            "driver": driver
        }


# Automatic demonstration data
if __name__ == "__main__":

    ride = RideBooking()

    result = ride.calculate(
        "C101",
        "Vellore",
        "Katpadi",
        10,
        2,
        "Sedan",
        12
    )

    print(result)
