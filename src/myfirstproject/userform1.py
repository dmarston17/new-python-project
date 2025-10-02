# This is my first GUI application using tkinter!
# It's a simple user management system where you can add, update, and delete users.

# Import the libraries we need
import tkinter as tk  # Main GUI library
from tkinter import messagebox, ttk  # For message boxes and better-looking widgets

# Main application class that handles all our form functionality
class UserFormApp:
    def __init__(self, root):
        """This is where we set up our application window and all its parts"""
        # root is the main window of our application
        self.root = root
        
        # Set window size (width x height) and title
        self.root.geometry("400x350")  # Make window 400 pixels wide and 350 pixels tall
        self.root.title("User Form CRUD")  # CRUD means Create, Read, Update, Delete
        
        # Make the background light blue - it looks nicer than plain gray!
        self.root.configure(bg="lightblue")

        # This list will store all our users
        # I'm using a simple list instead of a database to keep things simple for learning
        self.users = []  # Start with an empty list

        # Form Frame
        form_frame = tk.Frame(root, bg="lightblue")
        form_frame.pack(padx=10, pady=10, fill=tk.X)

        # Adding options for Username
        tk.Label(form_frame, text="Username:", bg="lightblue").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.username_entry = tk.Entry(form_frame)
        self.username_entry.grid(row=0, column=1, pady=5)

        # Adding options for Email
        tk.Label(form_frame, text="Email:", bg="lightblue").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.email_entry = tk.Entry(form_frame)
        self.email_entry.grid(row=1, column=1, pady=5)

        # Adding Buttons
        button_frame = tk.Frame(form_frame, bg="lightblue")
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        self.add_button = tk.Button(button_frame, text="Enter", bg="blue", fg="white", width=10, command=self.add_user)
        self.add_button.pack(side=tk.LEFT, padx=5)
        self.update_button = tk.Button(button_frame, text="Update", bg="orange", fg="white", width=10, command=self.update_user)
        self.update_button.pack(side=tk.LEFT, padx=5)
        self.delete_button = tk.Button(button_frame, text="Delete", bg="red", fg="white", width=10, command=self.delete_user)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        # Treeview to show users
        self.tree = ttk.Treeview(root, columns=("Username", "Email"), show="headings")
        self.tree.heading("Username", text="Username")
        self.tree.heading("Email", text="Email")
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.tree.bind('<<TreeviewSelect>>', self.on_user_select)

    def add_user(self):
        """Add a new user to our list and display it in the table"""
        # Get what the user typed in the username and email fields
        # strip() removes any extra spaces at the start or end
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        
        # Check if the user filled in both fields
        if not username or not email:
            messagebox.showwarning("Input Error", "Please fill in both fields.")
            return
        self.users.append({"username": username, "email": email})
        self.refresh_tree()
        self.clear_entries()
        messagebox.showinfo("Info", f"User {username} registered successfully!")

    def update_user(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a user to update.")
            return
        idx = int(selected[0])  # Treeview item id is index as string
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        if not username or not email:
            messagebox.showwarning("Input Error", "Please fill in both fields.")
            return
        self.users[idx] = {"username": username, "email": email}
        self.refresh_tree()
        self.clear_entries()

    def delete_user(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a user to delete.")
            return
        idx = int(selected[0])
        del self.users[idx]
        self.refresh_tree()
        self.clear_entries()

    def refresh_tree(self):
        # Clear all existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Insert all users
        for idx, user in enumerate(self.users):
            self.tree.insert("", "end", iid=str(idx), values=(user["username"], user["email"]))

    def clear_entries(self):
        self.username_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

    def on_user_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        idx = int(selected[0])
        user = self.users[idx]
        self.username_entry.delete(0, tk.END)
        self.username_entry.insert(0, user["username"])
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, user["email"])

if __name__ == "__main__":
    root = tk.Tk()
    app = UserFormApp(root)
    root.mainloop()