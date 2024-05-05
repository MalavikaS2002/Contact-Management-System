import tkinter as tk
from tkinter import messagebox
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Malavika@2002",
    database="contactmanager",
    auth_plugin='caching_sha2_password')

cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS contacts (name VARCHAR(20), phonenumber BIGINT(10))")

class ContactManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Management System")
        self.root.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        self.create_add_contact_frame()
        self.create_search_frame()
        self.create_results_frame()
        self.create_show_contacts_button()
        self.create_remove_frame()
        self.create_update_frame()

    def create_add_contact_frame(self):
        self.add_frame = tk.Frame(self.root, bg="#f0f0f0", bd=5)
        self.add_frame.place(relx=0.5, rely=0.05, relwidth=0.75, relheight=0.15, anchor="n")

        self.add_name_label = tk.Label(self.add_frame, text="Name:", bg="#f0f0f0", fg="#333333")
        self.add_name_label.grid(row=0, column=0, padx=10, pady=10)

        self.add_name_entry = tk.Entry(self.add_frame, bg="white", fg="#333333")
        self.add_name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.add_phone_label = tk.Label(self.add_frame, text="Phone:", bg="#f0f0f0", fg="#333333")
        self.add_phone_label.grid(row=0, column=2, padx=10, pady=10)

        self.add_phone_entry = tk.Entry(self.add_frame, bg="white", fg="#333333")
        self.add_phone_entry.grid(row=0, column=3, padx=10, pady=10)

        self.add_button = tk.Button(self.add_frame, text="Add Contact", bg="#2196f3", fg="white", command=self.add_contact)
        self.add_button.grid(row=0, column=4, padx=10, pady=10)

    def create_search_frame(self):
        self.search_frame = tk.Frame(self.root, bg="#f0f0f0", bd=5)
        self.search_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.1, anchor="n")

        self.search_entry = tk.Entry(self.search_frame, bg="white", fg="#333333")
        self.search_entry.place(relx=0, rely=0, relwidth=0.65, relheight=1)

        self.search_button = tk.Button(self.search_frame, text="Search", bg="#2196f3", fg="white", command=self.search_contact)
        self.search_button.place(relx=0.7, rely=0, relwidth=0.3, relheight=1)

    def create_results_frame(self):
        self.results_frame = tk.Frame(self.root, bg="#f0f0f0", bd=5)
        self.results_frame.place(relx=0.5, rely=0.4, relwidth=0.75, relheight=0.4, anchor="n")

        self.results_text = tk.Text(self.results_frame, bg="white", fg="#333333")
        self.results_text.place(relwidth=1, relheight=1)

    def create_show_contacts_button(self):
        self.show_contacts_button = tk.Button(self.root, text="Show Contacts", bg="black", fg="white", command=self.show_all_contacts)
        self.show_contacts_button.place(relx=0.5, rely=0.85, relwidth=0.75, relheight=0.1, anchor="n")

    def create_remove_frame(self):
        self.remove_frame = tk.Frame(self.root, bg="#f0f0f0", bd=5)
        self.remove_frame.place(relx=0.5, rely=0.95, relwidth=0.75, relheight=0.05, anchor="n")

        self.remove_label = tk.Label(self.remove_frame, text="Remove Contact (by name):", bg="#f0f0f0", fg="#333333")
        self.remove_label.place(relx=0.05, rely=0.1, relheight=0.8)

        self.remove_entry = tk.Entry(self.remove_frame, bg="white", fg="#333333")
        self.remove_entry.place(relx=0.35, rely=0.1, relwidth=0.5, relheight=0.8)

        self.remove_button = tk.Button(self.remove_frame, text="Remove", bg="#f44336", fg="white", command=self.remove_contact)
        self.remove_button.place(relx=0.9, rely=0.1, relwidth=0.1, relheight=0.8)

    def create_update_frame(self):
        self.update_frame = tk.Frame(self.root, bg="#f0f0f0", bd=5)
        self.update_frame.place(relx=0.5, rely=0.2, relwidth=0.75, relheight=0.05, anchor="n")

        self.update_label = tk.Label(self.update_frame, text="Update Phone Number (by name):", bg="#f0f0f0", fg="#333333")
        self.update_label.place(relx=0.05, rely=0.1, relheight=0.8)

        self.update_entry_name = tk.Entry(self.update_frame, bg="white", fg="#333333")
        self.update_entry_name.place(relx=0.35, rely=0.1, relwidth=0.3, relheight=0.8)

        self.update_entry_phone = tk.Entry(self.update_frame, bg="white", fg="#333333")
        self.update_entry_phone.place(relx=0.65, rely=0.1, relwidth=0.3, relheight=0.8)

        self.update_button = tk.Button(self.update_frame, text="Update", bg="#4caf50", fg="white", command=self.update_contact)
        self.update_button.place(relx=0.9, rely=0.1, relwidth=0.1, relheight=0.8)

    def add_contact(self):
        name = self.add_name_entry.get()
        phone = self.add_phone_entry.get()
        if name and phone:
            try:
                # Check if phone number length doesn't exceed 10 digits
                if len(phone) > 10:
                    raise ValueError("Phone number must not exceed 10 characters.")

                # Check if phone number starts with a digit between 0 and 9
                if not phone.isdigit() or not 0 <= int(phone[0]) <= 9:
                    raise ValueError("Phone number must start with a digit between 0 and 9.")

                query = "INSERT INTO contacts (name, phonenumber) VALUES (%s, %s)"
                contact = (name, phone)
                cursor.execute(query, contact)
                db.commit()
                messagebox.showinfo("Success", "Contact added successfully!")
                self.add_name_entry.delete(0, tk.END)
                self.add_phone_entry.delete(0, tk.END)
            except ValueError as ve:
                messagebox.showerror("Error", str(ve))
            except mysql.connector.Error as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Please fill in both name and phone fields.")

    def search_contact(self):
        query = self.search_entry.get().lower()
        cursor.execute("SELECT * FROM contacts WHERE LOWER(name) LIKE %s", ('%' + query + '%',))
        results = cursor.fetchall()
        if results:
            self.search_entry.delete(0, tk.END)
            self.results_text.delete(1.0, tk.END)
            for contact in results:
                self.results_text.insert(tk.END, f"Name: {contact[0]}\nPhone: {contact[1]}\n\n")
        else:
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, "No matching contacts found.")

    def show_all_contacts(self):
        cursor.execute("SELECT * FROM contacts")
        results = cursor.fetchall()
        if results:
            self.results_text.delete(1.0, tk.END)
            for contact in results:
                self.results_text.insert(tk.END, f"Name: {contact[0]}\nPhone: {contact[1]}\n\n")
        else:
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, "No contacts found.")

    def remove_contact(self):
        name = self.remove_entry.get()
        if name:
            try:
                cursor.execute("DELETE FROM contacts WHERE name = %s", (name,))
                db.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Success", f"Contact '{name}' removed successfully!")
                else:
                    messagebox.showerror("Error", f"No contact with name '{name}' found.")
            except mysql.connector.Error as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Please enter a name to remove.")

    def update_contact(self):
        name = self.update_entry_name.get()
        phone = self.update_entry_phone.get()
        if name and phone:
            try:
                # Check if phone number length doesn't exceed 10 digits
                if len(phone)>10:
                    raise ValueError("Phone number must not exceed 10 characters.")

                # Check if phone number starts with a digit between 0 and 9
                if not phone.isdigit() or not 0 <= int(phone[0]) <= 9:
                    raise ValueError("Phone number must start with a digit between 0 and 9.")

                cursor.execute("UPDATE contacts SET phonenumber = %s WHERE name = %s", (phone, name))
                db.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Success", f"Phone number for contact '{name}' updated successfully!")
                else:
                    messagebox.showerror("Error", f"No contact with name '{name}' found.")
            except ValueError as ve:
                messagebox.showerror("Error", str(ve))
            except mysql.connector.Error as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Please fill in both name and phone fields.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManagementSystem(root)
    root.mainloop()
