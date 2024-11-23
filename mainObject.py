import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from datetime import datetime
import re

class EmployeeManagementSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.create_variables()
        self.setup_database()
        self.create_ui()
        self.load_initial_data()

    def setup_window(self):
        """Configure the main window settings"""
        self.root.geometry("800x700")
        self.root.title("Employee Management System")
        self.root.config(bg="#06283D")
        self.root.resizable(True, True)

    def create_variables(self):
        """Create tkinter variables for form fields"""
        self.id_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.dob_var = tk.StringVar()
        self.gender_var = tk.StringVar()
        self.salary_var = tk.StringVar()

    def setup_database(self):
        """Initialize database connection"""
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Ngocchung241120",
                database="Company"
            )
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to connect to database:\n{err}")
            self.root.destroy()

    def create_ui(self):
        """Create the user interface"""
        # Header
        header = tk.Label(
            self.root,
            text="Employee Management System",
            font=("Helvetica", 16, "bold"),
            bg="#06283D",
            fg="white",
            pady=10
        )
        header.pack(pady=20)

        # Create main frame
        main_frame = tk.Frame(self.root, bg="#06283D")
        main_frame.pack(padx=20, pady=10)

        # Input fields
        fields = [
            ("Employee ID:", self.id_var),
            ("Full Name:", self.name_var),
            ("DOB (YYYY-MM-DD):", self.dob_var),
            ("Gender (M/F):", self.gender_var),
            ("Salary:", self.salary_var)
        ]

        for label_text, variable in fields:
            frame = tk.Frame(main_frame, bg="#06283D")
            frame.pack(pady=5, fill="x")
            
            label = tk.Label(
                frame,
                text=label_text,
                font=("Helvetica", 10),
                bg="#06283D",
                fg="white",
                width=20,
                anchor="w"
            )
            label.pack(side="left")
            
            entry = ttk.Entry(frame, textvariable=variable)
            entry.pack(side="left", expand=True, fill="x")

        # Buttons frame
        button_frame = tk.Frame(main_frame, bg="#06283D")
        button_frame.pack(pady=20)

        buttons = [
            ("Insert", self.insert),
            ("Update", self.update),
            ("Delete", self.delete),
            ("Get", self.get),
            ("Clear", self.clear_fields)
        ]

        for text, command in buttons:
            ttk.Button(
                button_frame,
                text=text,
                command=command,
                width=15
            ).pack(side="left", padx=5)

        # Create Treeview with scrollbar
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(tree_frame)
        y_scrollbar.pack(side="right", fill="y")

        x_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal")
        x_scrollbar.pack(side="bottom", fill="x")

        # Create and configure the Treeview
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "First Name", "Last Name", "DOB", "Gender", "Salary"),
            show="headings",
            yscrollcommand=y_scrollbar.set,
            xscrollcommand=x_scrollbar.set
        )

        # Configure scrollbars
        y_scrollbar.config(command=self.tree.yview)
        x_scrollbar.config(command=self.tree.xview)

        # Configure column headings and widths with correct anchor values
        column_configs = {
            "ID": (80, "center"),
            "First Name": (120, "w"),  # Changed from "left" to "w"
            "Last Name": (120, "w"),   # Changed from "left" to "w"
            "DOB": (100, "center"),
            "Gender": (80, "center"),
            "Salary": (100, "e")       # Changed from "right" to "e"
        }

        for col, (width, align) in column_configs.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=align)

        self.tree.pack(side="left", fill="both", expand=True)

        # Bind select event
        self.tree.bind('<<TreeviewSelect>>', self.item_selected)

    def validate_inputs(self):
        """Validate all input fields"""
        if not all([self.id_var.get(), self.name_var.get(), self.dob_var.get(),
                   self.gender_var.get(), self.salary_var.get()]):
            raise ValueError("All fields must be filled")

        # Validate ID
        if not self.id_var.get().isdigit():
            raise ValueError("Employee ID must be a number")

        # Validate name
        name_parts = self.name_var.get().split()
        if len(name_parts) < 2:
            raise ValueError("Please enter both first and last name")

        # Validate date format
        try:
            datetime.strptime(self.dob_var.get(), '%Y-%m-%d')
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")

        # Validate gender
        if self.gender_var.get().upper() not in ['M', 'F']:
            raise ValueError("Gender must be 'M' or 'F'")

        # Validate salary
        if not re.match(r'^\d+(\.\d{1,2})?$', self.salary_var.get()):
            raise ValueError("Invalid salary format")

    def load_initial_data(self):
        """Load and display data when the application starts"""
        try:
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Fetch all employees
            self.cursor.execute("""
                SELECT emp_id, first_name, last_name, birth_day, sex, salary 
                FROM employee 
                ORDER BY emp_id
            """)
            
            # Insert data into treeview
            for row in self.cursor.fetchall():
                # Format salary to 2 decimal places
                formatted_salary = f"{float(row[5]):,.2f}"
                # Format date to YYYY-MM-DD
                formatted_date = row[3].strftime('%Y-%m-%d') if row[3] else ''
                
                display_row = (
                    row[0],              # ID
                    row[1],              # First Name
                    row[2],              # Last Name
                    formatted_date,      # DOB
                    row[4],              # Gender
                    formatted_salary     # Salary
                )
                self.tree.insert('', 'end', values=display_row)

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to load data:\n{e}")

    def item_selected(self, event):
        """Handle item selection in Treeview"""
        selected_item = self.tree.selection()
        if selected_item:
            # Get the selected item's values
            values = self.tree.item(selected_item[0])['values']
            
            # Update entry fields with selected data
            self.id_var.set(values[0])
            self.name_var.set(f"{values[1]} {values[2]}")  # Combine first and last name
            self.dob_var.set(values[3])
            self.gender_var.set(values[4])
            self.salary_var.set(values[5])

    def insert(self):
        """Insert a new employee record"""
        try:
            self.validate_inputs()
            names = self.name_var.get().split()
            first_name = names[0]
            last_name = ' '.join(names[1:])

            query = """INSERT INTO employee 
                      (emp_id, first_name, last_name, birth_day, sex, salary) 
                      VALUES (%s, %s, %s, %s, %s, %s)"""
            values = (
                self.id_var.get(),
                first_name,
                last_name,
                self.dob_var.get(),
                self.gender_var.get().upper(),
                self.salary_var.get()
            )

            self.cursor.execute(query, values)
            self.conn.commit()
            messagebox.showinfo("Success", "Employee added successfully!")
            self.load_initial_data()
            self.clear_fields()

        except ValueError as e:
            messagebox.showerror("Validation Error", str(e))
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to insert record:\n{e}")

    def update(self):
        """Update an existing employee record"""
        try:
            self.validate_inputs()
            names = self.name_var.get().split()
            first_name = names[0]
            last_name = ' '.join(names[1:])

            query = """UPDATE employee 
                      SET first_name=%s, last_name=%s, birth_day=%s, sex=%s, salary=%s 
                      WHERE emp_id=%s"""
            values = (
                first_name,
                last_name,
                self.dob_var.get(),
                self.gender_var.get().upper(),
                self.salary_var.get(),
                self.id_var.get()
            )

            self.cursor.execute(query, values)
            self.conn.commit()
            messagebox.showinfo("Success", "Employee updated successfully!")
            self.load_initial_data()
            self.clear_fields()

        except ValueError as e:
            messagebox.showerror("Validation Error", str(e))
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to update record:\n{e}")

    def delete(self):
        """Delete an employee record"""
        if not self.id_var.get():
            messagebox.showerror("Error", "Please enter Employee ID to delete")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this employee?"):
            try:
                query = "DELETE FROM employee WHERE emp_id = %s"
                self.cursor.execute(query, (self.id_var.get(),))
                self.conn.commit()
                messagebox.showinfo("Success", "Employee deleted successfully!")
                self.load_initial_data()
                self.clear_fields()

            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Failed to delete record:\n{e}")

    def get(self):
        """Refresh the display with current database data"""
        self.load_initial_data()

    def clear_fields(self):
        """Clear all input fields"""
        for var in [self.id_var, self.name_var, self.dob_var, self.gender_var, self.salary_var]:
            var.set("")

    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = EmployeeManagementSystem()
    app.run()