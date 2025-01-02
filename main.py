import csv
from tkinter import *
from tkinter import messagebox


class Flight:
    def __init__(self, flight_id, departure, arrival, date, time, seats_available):
        self.flight_id = flight_id
        self.departure = departure
        self.arrival = arrival
        self.date = date
        self.time = time
        self.seats_available = int(seats_available)

    def to_csv_row(self):
        return [self.flight_id, self.departure, self.arrival, self.date, self.time, self.seats_available]


class Passenger:
    def __init__(self, passenger_id, name, contact_details, booked_flights):
        self.passenger_id = passenger_id
        self.name = name
        self.contact_details = contact_details
        self.booked_flights = booked_flights  

    def to_csv_row(self):
        return [self.passenger_id, self.name, self.contact_details, ",".join(self.booked_flights)]

    def can_book(self, flight_id):
        return flight_id not in self.booked_flights


class BookingManager:
    def __init__(self, flights_file, passengers_file, bookings_file):
        self.flights_file = flights_file
        self.passengers_file = passengers_file
        self.bookings_file = bookings_file
        self.flights = []
        self.passengers = []

        self.load_data()

    def load_data(self):
        
        with open(self.flights_file, "r") as file:
            reader = csv.reader(file)
            next(reader)  
            self.flights = [Flight(*row) for row in reader]

        
        with open(self.passengers_file, "r") as file:
            reader = csv.reader(file)
            next(reader)
            self.passengers = [Passenger(row[0], row[1], row[2], row[3].split(",")) for row in reader]

    def save_data(self):
        
        with open(self.flights_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Flight ID", "Departure", "Arrival", "Date", "Time", "Seats Available"])
            for flight in self.flights:
                writer.writerow(flight.to_csv_row())

        
        with open(self.passengers_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Passenger ID", "Name", "Contact Details", "Booked Flights"])
            for passenger in self.passengers:
                writer.writerow(passenger.to_csv_row())

    def find_flight(self, flight_id):
        for flight in self.flights:
            if flight.flight_id == flight_id:
                return flight
        return None

    def find_passenger(self, passenger_id):
        for passenger in self.passengers:
            if passenger.passenger_id == passenger_id:
                return passenger
        return None

    def book_flight(self, flight_id, passenger_id):
        flight = self.find_flight(flight_id)
        passenger = self.find_passenger(passenger_id)

        if not flight or not passenger:
            return "Flight or Passenger not found."

        if flight.seats_available <= 0:
            return "No seats available."

        if not passenger.can_book(flight_id):
            return "Passenger already booked this flight."

        
        flight.seats_available -= 1
        passenger.booked_flights.append(flight_id)
        self.save_data()
        return "Booking successful."

    def cancel_booking(self, flight_id, passenger_id):
        flight = self.find_flight(flight_id)
        passenger = self.find_passenger(passenger_id)

        if not flight or not passenger:
            return "Flight or Passenger not found."

        if flight_id not in passenger.booked_flights:
            return "No booking found for this flight."

        
        flight.seats_available += 1
        passenger.booked_flights.remove(flight_id)
        self.save_data()
        return "Booking canceled successfully."


class FlightBookingGUI:
    def __init__(self, manager):
        self.manager = manager
        self.root = Tk()
        self.root.title("Flight Booking System")

       
        Label(self.root, text="Flight Booking").grid(row=0, column=0, columnspan=2)
        Label(self.root, text="Flight ID").grid(row=1, column=0)
        self.flight_id_entry = Entry(self.root)
        self.flight_id_entry.grid(row=1, column=1)

        Label(self.root, text="Passenger ID").grid(row=2, column=0)
        self.passenger_id_entry = Entry(self.root)
        self.passenger_id_entry.grid(row=2, column=1)

        Button(self.root, text="Book Flight", command=self.book_flight).grid(row=3, column=0, columnspan=2)

        self.root.mainloop()

    def book_flight(self):
        flight_id = self.flight_id_entry.get()
        passenger_id = self.passenger_id_entry.get()
        result = self.manager.book_flight(flight_id, passenger_id)
        messagebox.showinfo("Result", result)


if __name__ == "__main__":
    manager = BookingManager("flights.csv", "passengers.csv", "bookings.csv")
    FlightBookingGUI(manager)
