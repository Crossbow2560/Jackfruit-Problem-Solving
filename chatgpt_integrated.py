import tkinter as tk
from tkinter import messagebox, ttk
from flight_booking_backend import BookingManager

class FlightBookingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Flight Booking System")
        self.root.geometry("800x600")
        
        # Initialize BookingManager with file paths
        self.manager = BookingManager("flights.csv", "passengers.csv", "bookings.csv")

        self.create_widgets()

    def create_widgets(self):
        # Title label
        title_label = tk.Label(self.root, text="Flight Booking System", font=("Arial", 20, "bold"), fg="blue")
        title_label.pack(pady=10)

        # Notebook for tabbed interface
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        # Tabs
        self.create_flight_tab()
        self.create_passenger_tab()
        self.create_booking_tab()

    def create_flight_tab(self):
        flight_tab = ttk.Frame(self.notebook)
        self.notebook.add(flight_tab, text="Flight Management")

        # Search bar for flights
        search_frame = tk.Frame(flight_tab)
        search_frame.pack(pady=10)
        tk.Label(search_frame, text="Search Flights:").pack(side=tk.LEFT, padx=5)
        self.flight_search_entry = tk.Entry(search_frame)
        self.flight_search_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Search", command=self.search_flights).pack(side=tk.LEFT, padx=5)

        # Schedule display button
        tk.Button(flight_tab, text="View Schedule", command=self.view_schedule).pack(pady=5)

        # Flight results area
        self.flight_results = tk.Text(flight_tab, height=15, width=80)
        self.flight_results.pack(pady=10)

    def create_passenger_tab(self):
        passenger_tab = ttk.Frame(self.notebook)
        self.notebook.add(passenger_tab, text="Passenger Management")

        # Search bar for passengers
        search_frame = tk.Frame(passenger_tab)
        search_frame.pack(pady=10)
        tk.Label(search_frame, text="Search Passengers:").pack(side=tk.LEFT, padx=5)
        self.passenger_search_entry = tk.Entry(search_frame)
        self.passenger_search_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Search", command=self.search_passengers).pack(side=tk.LEFT, padx=5)

        # Passenger details area
        self.passenger_details = tk.Text(passenger_tab, height=15, width=80)
        self.passenger_details.pack(pady=10)

    def create_booking_tab(self):
        booking_tab = ttk.Frame(self.notebook)
        self.notebook.add(booking_tab, text="Booking Management")

        # Booking form
        form_frame = tk.Frame(booking_tab)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Flight ID:").grid(row=0, column=0, padx=5, pady=5)
        self.flight_id_entry = tk.Entry(form_frame)
        self.flight_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Passenger ID:").grid(row=1, column=0, padx=5, pady=5)
        self.passenger_id_entry = tk.Entry(form_frame)
        self.passenger_id_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(form_frame, text="Book Flight", command=self.book_flight).grid(row=2, column=0, padx=5, pady=10)
        tk.Button(form_frame, text="Cancel Booking", command=self.cancel_booking).grid(row=2, column=1, padx=5, pady=10)

        # Booking confirmation area
        self.booking_results = tk.Text(booking_tab, height=10, width=80)
        self.booking_results.pack(pady=10)

    def search_flights(self):
        query = self.flight_search_entry.get()
        results = self.manager.search_flight(query)
        self.flight_results.delete(1.0, tk.END)
        if results:
            for result in results:
                self.flight_results.insert(tk.END, f"Flight ID: {result[0]}, Departure: {result[1]}, Arrival: {result[2]}, Date: {result[3]}, Time: {result[4]}, Seats Available: {result[5]}\n")
        else:
            self.flight_results.insert(tk.END, "No flights found matching the query.\n")

    def view_schedule(self):
        results = self.manager.view_schedule()
        self.flight_results.delete(1.0, tk.END)
        if results:
            for result in results:
                self.flight_results.insert(tk.END, f"Flight ID: {result[0]}, Departure: {result[1]}, Arrival: {result[2]}, Date: {result[3]}, Time: {result[4]}, Seats Available: {result[5]}\n")
        else:
            self.flight_results.insert(tk.END, "No flights available in the schedule.\n")

    def search_passengers(self):
        query = self.passenger_search_entry.get()
        results = self.manager.search_passenger(query)
        self.passenger_details.delete(1.0, tk.END)
        if results:
            for result in results:
                self.passenger_details.insert(tk.END, f"Passenger ID: {result[0]}, Name: {result[1]}, Contact: {result[2]}, Booked Flights: {result[3]}\n")
        else:
            self.passenger_details.insert(tk.END, "No passengers found matching the query.\n")

    def book_flight(self):
        flight_id = self.flight_id_entry.get()
        passenger_id = self.passenger_id_entry.get()
        message = self.manager.book_flight(flight_id, passenger_id)
        self.booking_results.delete(1.0, tk.END)
        self.booking_results.insert(tk.END, message + "\n")

    def cancel_booking(self):
        flight_id = self.flight_id_entry.get()
        passenger_id = self.passenger_id_entry.get()
        message = self.manager.cancel_booking(flight_id, passenger_id)
        self.booking_results.delete(1.0, tk.END)
        self.booking_results.insert(tk.END, message + "\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = FlightBookingGUI(root)
    root.mainloop()