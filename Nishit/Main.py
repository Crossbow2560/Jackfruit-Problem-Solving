import tkinter as tk
from tkinter import messagebox, ttk
from flight_booking_backend import BookingManager

class FlightBookingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Flight Booking System")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f8ff")  # Light blue background

        # Initialize BookingManager with file paths
        self.manager = BookingManager("flights.csv", "passengers.csv", "bookings.csv")

        self.create_widgets()

    def create_widgets(self):
        # Title label
        title_label = tk.Label(
            self.root, 
            text="Flight Booking System", 
            font=("Helvetica", 24, "bold"), 
            fg="#4682b4",  # Steel blue
            bg="#f0f8ff"
        )
        title_label.pack(pady=20)

        # Notebook for tabbed interface
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=20, pady=10)

        # Tabs
        self.create_flight_tab()
        self.create_passenger_tab()
        self.create_booking_tab()

    def create_flight_tab(self):
        flight_tab = ttk.Frame(self.notebook)
        self.notebook.add(flight_tab, text="Flight Management")

        # Styling frame
        search_frame = tk.Frame(flight_tab, bg="#f0f8ff")
        search_frame.pack(pady=10, fill="x")

        # Search bar for flights
        tk.Label(
            search_frame, text="Search Flights:", font=("Arial", 12), bg="#f0f8ff"
        ).pack(side=tk.LEFT, padx=10)

        self.flight_search_entry = tk.Entry(search_frame, font=("Arial", 12), width=30)
        self.flight_search_entry.pack(side=tk.LEFT, padx=10)

        tk.Button(
            search_frame, text="Search", font=("Arial", 12), bg="#87cefa", fg="white", command=self.search_flights
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            search_frame, text="View Schedule", font=("Arial", 12), bg="#4682b4", fg="white", command=self.view_schedule
        ).pack(side=tk.LEFT, padx=10)

        # Flight results area
        self.flight_results = tk.Text(flight_tab, font=("Courier", 10), bg="#f5f5f5", height=20, wrap="word")
        self.flight_results.pack(pady=10, padx=10, fill="both")

    def create_passenger_tab(self):
        passenger_tab = ttk.Frame(self.notebook)
        self.notebook.add(passenger_tab, text="Passenger Management")

        # Styling frame
        search_frame = tk.Frame(passenger_tab, bg="#f0f8ff")
        search_frame.pack(pady=10, fill="x")

        # Search bar for passengers
        tk.Label(
            search_frame, text="Search Passengers:", font=("Arial", 12), bg="#f0f8ff"
        ).pack(side=tk.LEFT, padx=10)

        self.passenger_search_entry = tk.Entry(search_frame, font=("Arial", 12), width=30)
        self.passenger_search_entry.pack(side=tk.LEFT, padx=10)

        tk.Button(
            search_frame, text="Search", font=("Arial", 12), bg="#87cefa", fg="white", command=self.search_passengers
        ).pack(side=tk.LEFT, padx=10)

        # Passenger details area
        self.passenger_details = tk.Text(passenger_tab, font=("Courier", 10), bg="#f5f5f5", height=20, wrap="word")
        self.passenger_details.pack(pady=10, padx=10, fill="both")

    def create_booking_tab(self):
        booking_tab = ttk.Frame(self.notebook)
        self.notebook.add(booking_tab, text="Booking Management")

        # Booking form frame
        form_frame = tk.Frame(booking_tab, bg="#f0f8ff")
        form_frame.pack(pady=20, fill="x")

        tk.Label(
            form_frame, text="Flight ID:", font=("Arial", 12), bg="#f0f8ff"
        ).grid(row=0, column=0, padx=10, pady=5, sticky="e")

        self.flight_id_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
        self.flight_id_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(
            form_frame, text="Passenger ID:", font=("Arial", 12), bg="#f0f8ff"
        ).grid(row=1, column=0, padx=10, pady=5, sticky="e")

        self.passenger_id_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
        self.passenger_id_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Button(
            form_frame, text="Book Flight", font=("Arial", 12), bg="#4682b4", fg="white", command=self.book_flight
        ).grid(row=2, column=0, padx=10, pady=10)

        tk.Button(
            form_frame, text="Cancel Booking", font=("Arial", 12), bg="#87cefa", fg="white", command=self.cancel_booking
        ).grid(row=2, column=1, padx=10, pady=10)

        # Booking results area
        self.booking_results = tk.Text(booking_tab, font=("Courier", 10), bg="#f5f5f5", height=15, wrap="word")
        self.booking_results.pack(pady=10, padx=10, fill="both")

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
