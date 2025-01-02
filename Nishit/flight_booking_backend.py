import csv
import os

class Flight:
    def __init__(self, flight_id, departure, arrival, date, time, seats_available):
        self.flight_id = flight_id
        self.departure = departure
        self.arrival = arrival
        self.date = date
        self.time = time
        self.seats_available = int(seats_available)

    def to_csv_format(self):
        return [self.flight_id, self.departure, self.arrival, self.date, self.time, self.seats_available]

class Passenger:
    def __init__(self, passenger_id, name, contact_details, booked_flights=None):
        self.passenger_id = passenger_id
        self.name = name
        self.contact_details = contact_details
        self.booked_flights = booked_flights if booked_flights else []

    def add_flight(self, flight_id):
        if flight_id not in self.booked_flights:
            self.booked_flights.append(flight_id)

    def remove_flight(self, flight_id):
        if flight_id in self.booked_flights:
            self.booked_flights.remove(flight_id)

    def to_csv_format(self):
        return [self.passenger_id, self.name, self.contact_details, ",".join(self.booked_flights)]

class BookingManager:
    def __init__(self, flights_file, passengers_file, bookings_file):
        self.flights_file = flights_file
        self.passengers_file = passengers_file
        self.bookings_file = bookings_file
        self.update_log_file = "updateLog.csv"
        self.flights = {}
        self.passengers = {}
        self.bookings = []
        self.load_data()

    def load_data(self):
        # Load flights
        try:
            with open(self.flights_file, mode='r') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                for row in reader:
                    flight = Flight(row[0], row[1], row[2], row[3], row[4], row[5])
                    self.flights[flight.flight_id] = flight
        except FileNotFoundError:
            print("Flights file not found. Starting fresh.")

        # Load passengers
        try:
            with open(self.passengers_file, mode='r') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                for row in reader:
                    booked_flights = row[3].split(',') if isinstance(row[3], str) and row[3] else []
                    passenger = Passenger(row[0], row[1], row[2], booked_flights)
                    self.passengers[passenger.passenger_id] = passenger
        except FileNotFoundError:
            print("Passengers file not found. Starting fresh.")

        # Load bookings
        try:
            with open(self.bookings_file, mode='r') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                self.bookings = list(reader)
        except FileNotFoundError:
            print("Bookings file not found. Starting fresh.")

    def save_flights(self):
        # Save flights
        with open(self.flights_file, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Flight ID", "Departure", "Arrival", "Date", "Time", "Seats Available"])
            for flight in self.flights.values():
                writer.writerow(flight.to_csv_format())

    def save_passengers(self):
        # Save passengers
        with open(self.passengers_file, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Passenger ID", "Name", "Contact Details", "Booked Flights"])
            for passenger in self.passengers.values():
                writer.writerow(passenger.to_csv_format())

    def save_bookings(self):
        # Save bookings
        with open(self.bookings_file, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Transaction Type", "Flight ID", "Passenger ID", "Date"])
            writer.writerows(self.bookings)

    def delete_booking(self, flight_id, passenger_id):
        with open(self.bookings_file, mode = 'r') as f:
            reader = csv.reader(f)
            self.data = []
            for row in reader:
                if row[0] == 'CANCEL' and row[1] == flight_id and row[2] == passenger_id:
                    pass
                else:
                    self.data.append(row)
        with open(self.bookings_file, mode = 'w', newline = '') as f:
            writer = csv.writer(f)
            writer.writerows(self.data)

    def log_update(self, transaction_type, flight_id, passenger_id):
        # Log the update into updateLog.csv
        log_exists = os.path.exists(self.update_log_file)
        with open(self.update_log_file, mode='a', newline='') as f:
            writer = csv.writer(f)
            if not log_exists:
                writer.writerow(["Transaction Type", "Flight ID", "Passenger ID", "Timestamp"])
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([transaction_type, flight_id, passenger_id, timestamp])

    def view_schedule(self):
        return [flight.to_csv_format() for flight in self.flights.values()]

    def search_flight(self, query):
        results = []
        for flight in self.flights.values():
            if query.lower() in (flight.flight_id + flight.departure + flight.arrival).lower():
                results.append(flight.to_csv_format())
        return results

    def search_passenger(self, query):
        results = []
        for passenger in self.passengers.values():
            if query.lower() in (passenger.passenger_id + passenger.name + passenger.contact_details).lower():
                results.append(passenger.to_csv_format())
        return results

    def book_flight(self, flight_id, passenger_id):
        if flight_id in self.flights and passenger_id in self.passengers:
            flight = self.flights[flight_id]
            passenger = self.passengers[passenger_id]
            if flight.seats_available > 0 and flight_id not in passenger.booked_flights:
                flight.seats_available -= 1
                passenger.add_flight(flight_id)
                self.bookings.append(["BOOK", flight_id, passenger_id, flight.date])
                self.save_flights()
                self.save_bookings()
                self.save_passengers()
                self.log_update("BOOK", flight_id, passenger_id)
                return f"Flight {flight_id} booked successfully for passenger {passenger_id}."
            return "Booking failed: No seats available or duplicate booking."
        return "Booking failed: Flight or passenger not found."

    def cancel_booking(self, flight_id, passenger_id):
        if flight_id in self.flights and passenger_id in self.passengers:
            flight = self.flights[flight_id]
            passenger = self.passengers[passenger_id]
            if flight_id in passenger.booked_flights:
                flight.seats_available += 1
                passenger.remove_flight(flight_id)
                self.bookings.append(["CANCEL", flight_id, passenger_id, flight.date])
                self.save_flights()
                self.save_bookings()
                self.save_passengers()
                # self.delete_booking(flight_id, passenger_id)
                self.log_update("CANCEL", flight_id, passenger_id)
                return f"Booking for flight {flight_id} canceled for passenger {passenger_id}."
            return "Cancellation failed: Booking not found."
        return "Cancellation failed: Flight or passenger not found."
