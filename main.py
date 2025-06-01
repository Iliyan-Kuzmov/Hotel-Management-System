import tkinter as tk
from tkinter import messagebox
import os

class HotelApp:
    def __init__(self):
        self.login_window()

    def login_window(self):
        self.root = tk.Tk()
        self.root.configure(bg="#6a0dad")
        self.root.geometry('400x300')
        self.root.title("Login")

        tk.Label(self.root, text="Login", font=('Helvetica', 20, 'bold'), bg="#6a0dad", fg="white").pack(pady=20)

        tk.Label(self.root, text="Username", bg="#6a0dad", fg="white").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Password", bg="#6a0dad", fg="white").pack()
        self.password_entry = tk.Entry(self.root, show='*')
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Login", command=self.check_login, bg="white", fg="#6a0dad", font=('Helvetica', 10, 'bold')).pack(pady=20)

        self.root.mainloop()

    def check_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    parts = line.strip().split()
                    if len(parts) >= 2 and parts[0] == username and parts[1] == password:
                        self.root.destroy()
                        self.main_window()
                        return
            messagebox.showerror("Login Failed", "Invalid username or password")
        except FileNotFoundError:
            messagebox.showerror("Error", "users.txt not found")

    def main_window(self):
        self.main = tk.Tk()
        self.main.title("Hotel Management System")
        self.main.geometry('600x500')
        self.main.configure(bg="#f0f0f5")

        tk.Label(self.main, text="Hotel Dashboard", font=('Helvetica', 20, 'bold'), bg="#f0f0f5").pack(pady=20)

        tk.Button(self.main, text="View Rooms", width=30, command=self.show_rooms, bg="#6a0dad", fg="white").pack(pady=10)
        tk.Button(self.main, text="View Guests", width=30, command=self.show_guests, bg="#6a0dad", fg="white").pack(pady=10)
        tk.Button(self.main, text="Add New Guest", width=30, command=self.show_new_guest, bg="#6a0dad", fg="white").pack(pady=10)
        tk.Button(self.main, text="Search Guest by Name", width=30, command=self.search_guest, bg="#6a0dad", fg="white").pack(pady=10)
        tk.Button(self.main, text="Free a Room", width=30, command=self.free_room_window, bg="#6a0dad", fg="white").pack(pady=10)
        tk.Button(self.main, text="Statistics", width=30, command=self.show_statistics, bg="#6a0dad", fg="white").pack(pady=10)

        self.main.mainloop()

    def show_rooms(self):
        win = tk.Toplevel(self.main)
        win.title("Rooms")
        win.geometry('400x400')

        tk.Label(win, text="All Rooms", font=('Arial', 14)).pack(pady=10)
        rooms_text = tk.Text(win, height=10, width=40)
        rooms_text.pack()

        try:
            with open("rooms.txt", "r") as file:
                rooms_text.insert(tk.END, file.read())
        except FileNotFoundError:
            rooms_text.insert(tk.END, "rooms.txt not found")

        tk.Button(win, text="Show Free Rooms", command=lambda: self.show_free_rooms(rooms_text)).pack(pady=10)

    def show_free_rooms(self, text_widget):
        text_widget.delete('1.0', tk.END)
        try:
            with open("rooms.txt", "r") as file:
                for line in file:
                    parts = line.strip().split()
                    if parts[-1] == "1":
                        text_widget.insert(tk.END, line + '\n')
        except FileNotFoundError:
            text_widget.insert(tk.END, "rooms.txt not found")

    def show_guests(self):
        win = tk.Toplevel(self.main)
        win.title("Guests")
        win.geometry('400x400')

        tk.Label(win, text="All Guests", font=('Arial', 14)).pack(pady=10)
        guests_text = tk.Text(win, height=15, width=40)
        guests_text.pack()

        try:
            with open("guests.txt", "r") as file:
                guests_text.insert(tk.END, file.read())
        except FileNotFoundError:
            guests_text.insert(tk.END, "guests.txt not found")

    def show_new_guest(self):
        win = tk.Toplevel(self.main)
        win.title("Add New Guest")
        win.geometry('400x400')

        tk.Label(win, text="New Guest Details", font=('Arial', 14)).pack(pady=10)

        tk.Label(win, text="Name").pack()
        name_entry = tk.Entry(win)
        name_entry.pack(pady=5)

        tk.Label(win, text="EGN").pack()
        egn_entry = tk.Entry(win)
        egn_entry.pack(pady=5)

        tk.Label(win, text="Room Number").pack()
        room_entry = tk.Entry(win)
        room_entry.pack(pady=5)

        def save_guest():
            name = name_entry.get().strip()
            egn = egn_entry.get().strip()
            room = room_entry.get().strip()

            if not name or not egn or not room:
                messagebox.showerror("Error", "All fields are required")
                return

            try:
                updated_rooms = []
                room_found = False
                room_free = False

                with open("rooms.txt", "r") as file:
                    for line in file:
                        parts = line.strip().split()
                        if parts[0] == room:
                            room_found = True
                            if parts[-1] == "1":
                                parts[-1] = "0"
                                room_free = True
                            line = " ".join(parts)
                        updated_rooms.append(line)

                if not room_found:
                    messagebox.showerror("Error", "Room not found")
                    return
                if not room_free:
                    messagebox.showerror("Error", "Room is occupied")
                    return

                with open("guests.txt", "a") as gfile:
                    gfile.write(f"{name} {egn} {room}\n")

                with open("rooms.txt", "w") as rfile:
                    rfile.write("\n".join(updated_rooms) + "\n")

                messagebox.showinfo("Success", "Guest added successfully")
                win.destroy()

            except FileNotFoundError:
                messagebox.showerror("Error", "Required files not found")

        tk.Button(win, text="Save Guest", command=save_guest, bg="#6a0dad", fg="white").pack(pady=20)

    def search_guest(self):
        win = tk.Toplevel(self.main)
        win.title("Search Guest")
        win.geometry("400x200")

        tk.Label(win, text="Enter guest name:").pack(pady=5)
        name_entry = tk.Entry(win)
        name_entry.pack(pady=5)

        result_label = tk.Label(win, text="")
        result_label.pack(pady=10)

        def perform_search():
            name = name_entry.get().strip().lower()
            try:
                with open("guests.txt", "r") as file:
                    for line in file:
                        if name in line.lower():
                            result_label.config(text=line.strip())
                            return
                result_label.config(text="Guest not found")
            except FileNotFoundError:
                result_label.config(text="guests.txt not found")

        tk.Button(win, text="Search", command=perform_search).pack(pady=5)

    def free_room_window(self):
        win = tk.Toplevel(self.main)
        win.title("Free a Room")
        win.geometry("400x200")

        tk.Label(win, text="Enter room number to free:").pack(pady=10)
        room_entry = tk.Entry(win)
        room_entry.pack(pady=5)

        def free_room():
            room = room_entry.get().strip()
            updated_rooms = []
            freed = False
            try:
                with open("rooms.txt", "r") as file:
                    for line in file:
                        parts = line.strip().split()
                        if parts[0] == room and parts[-1] == "0":
                            parts[-1] = "1"
                            freed = True
                        updated_rooms.append(" ".join(parts))
                with open("rooms.txt", "w") as file:
                    file.write("\n".join(updated_rooms) + "\n")
                if freed:
                    messagebox.showinfo("Success", f"Room {room} is now free.")
                else:
                    messagebox.showerror("Error", f"Room {room} is already free or not found.")
            except FileNotFoundError:
                messagebox.showerror("Error", "rooms.txt not found")

        tk.Button(win, text="Free Room", command=free_room, bg="#6a0dad", fg="white").pack(pady=10)

    def show_statistics(self):
        win = tk.Toplevel(self.main)
        win.title("Statistics")
        win.geometry("400x200")

        try:
            total_rooms = 0
            free_rooms = 0
            with open("rooms.txt", "r") as file:
                for line in file:
                    total_rooms += 1
                    if line.strip().endswith("1"):
                        free_rooms += 1

            with open("guests.txt", "r") as file:
                total_guests = len(file.readlines())

            stats = f"Total Rooms: {total_rooms}\nFree Rooms: {free_rooms}\nTotal Guests: {total_guests}"
        except FileNotFoundError:
            stats = "Some files not found"

        tk.Label(win, text=stats, font=('Arial', 12), justify="left").pack(pady=20)

if __name__ == '__main__':
    HotelApp()