import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

class DatabaseManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Company Database Management System")
        self.root.geometry("800x600")
        self.root.configure(bg="#06283D")

        # Database connection parameters
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'Ngocchung241120',
            'database': 'company'
        }

        # Table configuration
        self.tables = {
            'employee': {
                'columns': ['emp_id', 'first_name', 'last_name', 'birth_day', 'sex', 'salary', 'branch_id'],
                'primary_key': 'emp_id',
                'input_fields': ['ID', 'First Name', 'Last Name', 'Birth Day', 'Sex', 'Salary', 'Branch ID']
            },
            'branch': {
                'columns': ['branch_id', 'branch_name'],
                'primary_key': 'branch_id',
                'input_fields': ['Branch ID', 'Branch Name']
            },
            'client': {
                'columns': ['client_id', 'client_name', 'branch_id'],
                'primary_key': 'client_id',
                'input_fields': ['Client ID', 'Client Name', 'Branch ID']
            },
            'works_with': {
                'columns': ['emp_id', 'client_id', 'total_sales'],
                'primary_key': ['emp_id', 'client_id'],
                'input_fields': ['Employee ID', 'Client ID', 'Total Sales']
            }
        }

        self.setup_ui()

    def setup_ui(self):
        # Table Selection Dropdown
        self.table_var = tk.StringVar(self.root)
        self.table_var.set(list(self.tables.keys())[0])
        table_dropdown = ttk.Combobox(
            self.root, 
            textvariable=self.table_var, 
            values=list(self.tables.keys()),
            state="readonly",
            width=20
        )
        table_dropdown.place(x=20, y=20)
        table_dropdown.bind('<<ComboboxSelected>>', self.on_table_select)

        # Input Frame
        self.input_frame = tk.Frame(self.root, bg="#06283D")
        self.input_frame.place(x=20, y=60, width=760, height=150)

        # Create dynamic input fields
        self.entry_fields = {}
        self.setup_input_fields()

        # Buttons
        button_frame = tk.Frame(self.root, bg="#06283D")
        button_frame.place(x=20, y=220, width=760, height=40)

        buttons = [
            ("Insert", self.insert_record),
            ("Update", self.update_record),
            ("Delete", self.delete_record)
        ]

        for text, command in buttons:
            btn = tk.Button(
                button_frame, 
                text=text, 
                command=command, 
                bg="white", 
                font=("Arial", 10)
            )
            btn.pack(side=tk.LEFT, padx=5)

        # Treeview
        self.tree = ttk.Treeview(self.root)
        self.tree.place(x=20, y=270, width=760, height=300)

        # Scrollbars
        y_scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.tree.yview)
        y_scrollbar.place(x=780, y=270, height=300)
        
        x_scrollbar = ttk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=self.tree.xview)
        x_scrollbar.place(x=20, y=570, width=760)

        self.tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)

        # Initial load
        self.load_table_data()

    def setup_input_fields(self):
        # Clear existing fields
        for widget in self.input_frame.winfo_children():
            widget.destroy()

        # Get current table configuration
        table = self.tables[self.table_var.get()]
        columns = table['input_fields']

        # Create entry fields dynamically
        self.entry_fields = {}
        for i, col in enumerate(columns):
            label = tk.Label(
                self.input_frame, 
                text=col, 
                bg="#06283D", 
                fg="white", 
                font=("Arial", 10)
            )
            label.grid(row=i//3, column=(i%3)*2, padx=5, pady=5, sticky='e')

            entry = tk.Entry(self.input_frame, width=20)
            entry.grid(row=i//3, column=(i%3)*2 + 1, padx=5, pady=5)
            self.entry_fields[col] = entry

    def on_table_select(self, event=None):
        # Reset input fields when table changes
        self.setup_input_fields()
        self.load_table_data()

    def get_connection(self):
        return mysql.connector.connect(**self.db_config)

    def load_table_data(self):
        # Clear existing tree data
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Get current table configuration
        table = self.table_var.get()
        columns = self.tables[table]['columns']

        # Configure treeview
        self.tree['columns'] = columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')

        # Fetch and display data
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table}")
            
            for row in cursor.fetchall():
                self.tree.insert('', 'end', values=row)
            
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))

    def on_tree_select(self, event):
        # Populate input fields when a row is selected
        selected_item = self.tree.selection()
        if not selected_item:
            return

        values = self.tree.item(selected_item[0])['values']
        table = self.table_var.get()
        columns = self.tables[table]['input_fields']

        # Clear existing entries
        for entry in self.entry_fields.values():
            entry.delete(0, tk.END)

        # Populate entries with selected row data
        for i, col in enumerate(columns):
            if i < len(values):
                self.entry_fields[col].insert(0, str(values[i]))

    def insert_record(self):
        table = self.table_var.get()
        columns = self.tables[table]['columns']
        input_fields = self.tables[table]['input_fields']

        # Collect values from input fields
        values = [
            self.entry_fields[field].get() for field in input_fields
        ]

        # Validate input
        if any(val.strip() == '' for val in values):
            messagebox.showwarning("Input Error", "Please fill all fields")
            return

        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Create dynamic insert query
            placeholders = ', '.join(['%s'] * len(columns))
            query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
            
            cursor.execute(query, values)
            conn.commit()
            
            messagebox.showinfo("Success", "Record inserted successfully")
            
            # Refresh table view
            self.load_table_data()
            
            # Clear input fields
            for entry in self.entry_fields.values():
                entry.delete(0, tk.END)
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def update_record(self):
        table = self.table_var.get()
        columns = self.tables[table]['columns']
        input_fields = self.tables[table]['input_fields']
        primary_key = self.tables[table]['primary_key']

        # Collect values from input fields
        values = [
            self.entry_fields[field].get() for field in input_fields
        ]

        # Validate input
        if any(val.strip() == '' for val in values):
            messagebox.showwarning("Input Error", "Please fill all fields")
            return

        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Determine update and where conditions
            if isinstance(primary_key, list):
                # Composite primary key
                where_conditions = [f"{pk} = %s" for pk in primary_key]
                where_values = [values[columns.index(pk)] for pk in primary_key]
                update_columns = [col for col in columns if col not in primary_key]
                
                # Update query for composite key
                set_clause = ', '.join([f"{col} = %s" for col in update_columns])
                update_values = [
                    values[columns.index(col)] for col in update_columns
                ] + where_values

                query = f"UPDATE {table} SET {set_clause} WHERE {' AND '.join(where_conditions)}"
            else:
                # Single primary key
                primary_key_value = values[columns.index(primary_key)]
                update_columns = [col for col in columns if col != primary_key]
                
                # Update query for single key
                set_clause = ', '.join([f"{col} = %s" for col in update_columns])
                update_values = [
                    values[columns.index(col)] for col in update_columns
                ] + [primary_key_value]

                query = f"UPDATE {table} SET {set_clause} WHERE {primary_key} = %s"

            cursor.execute(query, update_values)
            conn.commit()
            
            messagebox.showinfo("Success", "Record updated successfully")
            
            # Refresh table view
            self.load_table_data()
            
            # Clear input fields
            for entry in self.entry_fields.values():
                entry.delete(0, tk.END)
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def delete_record(self):
        table = self.table_var.get()
        primary_key = self.tables[table]['primary_key']

        # Validate input for delete
        if isinstance(primary_key, list):
            # For composite primary key, need multiple values
            values = [
                self.entry_fields[self.tables[table]['input_fields'][columns.index(pk)]].get() 
                for pk in primary_key
            ]
            if any(val.strip() == '' for val in values):
                messagebox.showwarning("Input Error", "Please fill all primary key fields")
                return
        else:
            # For single primary key
            value = self.entry_fields[self.tables[table]['input_fields'][0]].get()
            if value.strip() == '':
                messagebox.showwarning("Input Error", "Please enter primary key value")
                return

        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Delete query generation
            if isinstance(primary_key, list):
                # Composite primary key
                where_conditions = [f"{pk} = %s" for pk in primary_key]
                query = f"DELETE FROM {table} WHERE {' AND '.join(where_conditions)}"
            else:
                # Single primary key
                query = f"DELETE FROM {table} WHERE {primary_key} = %s"

            cursor.execute(query, values if isinstance(primary_key, list) else [value])
            conn.commit()
            
            messagebox.showinfo("Success", "Record deleted successfully")
            
            # Refresh table view
            self.load_table_data()
            
            # Clear input fields
            for entry in self.entry_fields.values():
                entry.delete(0, tk.END)
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

def main():
    root = tk.Tk()
    app = DatabaseManagementApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()