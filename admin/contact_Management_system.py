import tkinter as tk
from tkinter import ttk, messagebox

# Linked List Node for contacts
class ContactNode:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone
        self.next = None

# Linked List to manage contacts
class ContactLinkedList:
    def __init__(self):
        self.head = None

    def add_contact(self, name, phone):
        new_node = ContactNode(name, phone)
        if self.head is None:
            self.head = new_node
        else:
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = new_node

    def delete_contact(self, name):
        temp = self.head
        if temp is not None:
            if temp.name == name:
                self.head = temp.next
                return True
            while temp.next is not None:
                if temp.next.name == name:
                    temp.next = temp.next.next
                    return True
                temp = temp.next
        return False

    def search_contact(self, name):
        temp = self.head
        while temp is not None:
            if temp.name.lower() == name.lower():  # Case insensitive search
                return temp.phone
            temp = temp.next
        return None

    def update_contact(self, old_name, new_name, new_phone):
        temp = self.head
        while temp is not None:
            if temp.name == old_name:
                temp.name = new_name
                temp.phone = new_phone
                return True
            temp = temp.next
        return False

    def display_contacts(self):
        contacts = []
        temp = self.head
        while temp is not None:
            contacts.append((temp.name, temp.phone))
            temp = temp.next
        return contacts

    def sort_contacts(self):
        if self.head is None:
            return
        sorted_list = []
        temp = self.head
        while temp:
            sorted_list.append((temp.name, temp.phone))
            temp = temp.next
        sorted_list.sort(key=lambda x: x[0])  # Sort by name
        self.head = None  # Clear the current list
        for name, phone in sorted_list:
            self.add_contact(name, phone)

# Hash Table for quick contact lookup
class ContactHashTable:
    def __init__(self, size=100):
        self.size = size
        self.table = [None] * size

    def hash_function(self, key):
        return hash(key) % self.size

    def add_contact(self, name, phone):
        index = self.hash_function(name)
        if not self.table[index]:
            self.table[index] = ContactLinkedList()
        self.table[index].add_contact(name, phone)

    def delete_contact(self, name):
        index = self.hash_function(name)
        if self.table[index]:
            return self.table[index].delete_contact(name)
        return False

    def update_contact(self, old_name, new_name, new_phone):
        index = self.hash_function(old_name)
        if self.table[index]:
            return self.table[index].update_contact(old_name, new_name, new_phone)
        return False

    def search_contact(self, name):
        index = self.hash_function(name)
        if self.table[index]:
            return self.table[index].search_contact(name)
        return None

    def display_all_contacts(self):
        all_contacts = []
        for linked_list in self.table:
            if linked_list:
                all_contacts.extend(linked_list.display_contacts())
        return all_contacts

    def sort_all_contacts(self):
        for linked_list in self.table:
            if linked_list:
                linked_list.sort_contacts()

# Login Page
class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Page")
        self.root.geometry("400x300")
        self.root.configure(bg="#e6f7ff")

        # Login label
        self.login_label = tk.Label(root, text="Login", font=("Arial", 20, "bold"), bg="#e6f7ff")
        self.login_label.pack(pady=20)

        # Username field
        self.username_label = tk.Label(root, text="Username:", font=("Arial", 14), bg="#e6f7ff")
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(root, font=("Arial", 14))
        self.username_entry.pack(pady=5)

        # Password field
        self.password_label = tk.Label(root, text="Password:", font=("Arial", 14), bg="#e6f7ff")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(root, font=("Arial", 14), show="*")
        self.password_entry.pack(pady=5)

        # Login button
        self.login_button = tk.Button(root, text="Login", font=("Arial", 14, "bold"), bg="#32cd32", fg="black", command=self.login)
        self.login_button.pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Simple username/password check
        if username == "admin" and password == "password":
            self.root.destroy()
            main_app = tk.Tk()
            ContactManagementApp(main_app)
            main_app.mainloop()
        else:
            messagebox.showerror("Error", "Invalid credentials. Try again.")

# Contact Management System GUI
class ContactManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Management System")
        self.root.geometry("700x500")

        # Initialize the contact hash table
        self.contact_table = ContactHashTable()

        # New theme color background
        self.root.configure(bg="#e6f7ff")

        # Setting up the header label with a creative font and color
        self.title_label = tk.Label(root, text="Contact Management System", font=("Comic Sans MS", 24, "bold"), fg="#ff6347", bg="#e6f7ff")
        self.title_label.pack(pady=20)

        # Name and Phone entry fields
        self.name_label = tk.Label(root, text="Name:", font=("Helvetica", 14, "italic"), fg="#4682b4", bg="#e6f7ff")
        self.name_label.pack()
        self.name_entry = tk.Entry(root, font=("Helvetica", 14), width=30)
        self.name_entry.pack(pady=5)

        self.phone_label = tk.Label(root, text="Phone:", font=("Helvetica", 14, "italic"), fg="#4682b4", bg="#e6f7ff")
        self.phone_label.pack()
        self.phone_entry = tk.Entry(root, font=("Helvetica", 14), width=30)
        self.phone_entry.pack(pady=5)

        # Contact list table
        self.contact_tree = ttk.Treeview(root, columns=("Name", "Phone"), show="headings", height=8)
        self.contact_tree.heading("Name", text="Name")
        self.contact_tree.heading("Phone", text="Phone")
        self.contact_tree.column("Name", width=200)
        self.contact_tree.column("Phone", width=150)

        # Buttons
        self.add_button = tk.Button(root, text="Add Contact", font=("Verdana", 14, "bold"), bg="#32cd32", fg="black", command=self.add_contact)
        self.add_button.pack(pady=5)

        self.update_button = tk.Button(root, text="Update Selected Contact", font=("Verdana", 14, "bold"), bg="#1e90ff", fg="black", command=self.select_contact_for_update)
        self.update_button.pack(pady=5)

        self.done_button = tk.Button(root, text="Done", font=("Verdana", 14, "bold"), bg="#32cd32", fg="black", command=self.finish_update)
        self.done_button.pack(pady=5)
        self.done_button.pack_forget()  # Hide the Done button by default

        self.delete_button = tk.Button(root, text="Delete Selected Contact", font=("Verdana", 14, "bold"), bg="#ff4500", fg="black", command=self.delete_selected_contact)
        self.delete_button.pack(pady=5)

        self.show_button = tk.Button(root, text="Show All Contacts", font=("Verdana", 14, "bold"), bg="#9370db", fg="black", command=self.show_contacts)
        self.show_button.pack(pady=5)

        self.sort_button = tk.Button(root, text="Sort Contacts (A-Z)", font=("Verdana", 14, "bold"), bg="#ffa500", fg="black", command=self.sort_contacts)
        self.sort_button.pack(pady=5)

        self.search_button = tk.Button(root, text="Search Contact", font=("Verdana", 14, "bold"), bg="#4682b4", fg="white", command=self.search_contact)
        self.search_button.pack(pady=5)

        self.selected_contact = None

    # Adding contact logic
    def add_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        if name and phone:
            self.contact_table.add_contact(name, phone)
            messagebox.showinfo("Success", f"Contact {name} added!")
            self.name_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)
            self.update_contact_tree()
        else:
            messagebox.showerror("Error", "Please enter both Name and Phone!")

    # Show all contacts in the table
    def show_contacts(self):
        self.contact_tree.pack(pady=10)  # Show the table when button is clicked
        self.update_contact_tree()  # Update the display

    # Sorting contacts
    def sort_contacts(self):
        self.contact_table.sort_all_contacts()  # Sort the contacts
        self.update_contact_tree()  # Update the display
        messagebox.showinfo("Success", "Contacts sorted alphabetically!")

    # Searching for a contact
    def search_contact(self):
        search_name = self.name_entry.get()
        if search_name:
            phone = self.contact_table.search_contact(search_name)
            if phone:
                messagebox.showinfo("Contact Found", f"Name: {search_name}\nPhone: {phone}")
                self.name_entry.delete(0, tk.END)
                self.phone_entry.delete(0, tk.END)
                self.name_entry.insert(0, search_name)
                self.phone_entry.insert(0, phone)
            else:
                messagebox.showerror("Error", "Contact not found!")
        else:
            messagebox.showerror("Error", "Please enter a name to search!")

    # Deleting the selected contact
    def delete_selected_contact(self):
        selected_item = self.contact_tree.selection()
        if selected_item:
            name = self.contact_tree.item(selected_item, "values")[0]
            if self.contact_table.delete_contact(name):
                messagebox.showinfo("Success", f"Contact {name} deleted!")
                self.update_contact_tree()
            else:
                messagebox.showerror("Error", "Contact not found!")
        else:
            messagebox.showerror("Error", "Please select a contact to delete!")

    # Update the table with all contacts
    def update_contact_tree(self):
        for i in self.contact_tree.get_children():
            self.contact_tree.delete(i)
        contacts = self.contact_table.display_all_contacts()
        for contact in contacts:
            self.contact_tree.insert("", tk.END, values=contact)

    # Select contact for update
    def select_contact_for_update(self):
        selected_item = self.contact_tree.selection()
        if selected_item:
            self.selected_contact = self.contact_tree.item(selected_item, "values")[0]
            self.name_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)

            # Fill the entry fields with selected contact details
            self.name_entry.insert(0, self.selected_contact)
            self.phone_entry.insert(0, self.contact_tree.item(selected_item, "values")[1])
            self.done_button.pack(pady=5)  # Show the Done button
        else:
            messagebox.showerror("Error", "Please select a contact to update!")

    # Finish update logic
    def finish_update(self):
        new_name = self.name_entry.get()
        new_phone = self.phone_entry.get()
        if self.selected_contact and new_name and new_phone:
            if self.contact_table.update_contact(self.selected_contact, new_name, new_phone):
                messagebox.showinfo("Success", f"Contact {self.selected_contact} updated to {new_name}!")
                self.selected_contact = None
                self.done_button.pack_forget()  # Hide the Done button
                self.update_contact_tree()
                self.name_entry.delete(0, tk.END)
                self.phone_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Update failed!")
        else:
            messagebox.showerror("Error", "Please enter both Name and Phone!")

# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    LoginPage(root)
    root.mainloop()
