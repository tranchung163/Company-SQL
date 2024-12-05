from tkinter import *
import tkinter.messagebox as MessageBox
import mysql.connector as mysql
from datetime import datetime
from tkinter import ttk

# Database configuration
PASSWORD = "Ngocchung241120"
DB_NAME = "company"

# Table configurations
TABLE_CONFIGS = {
    "employee": {
        "columns": ["emp_id", "first_name", "last_name", "birth_day", "sex", "salary", "branch_id"],
        "labels": ["Employee ID", "Full Name", "Date of Birth", "Sex", "Salary", "Branch"]
    },
    "branch": {
        "columns": ["branch_id", "branch_name"],
        "labels": ["Branch ID", "Branch Name"]
    },
    "client": {
        "columns": ["client_id", "client_name", "branch_id"],
        "labels": ["Client ID", "Client Name", "Branch ID"]
    },
    "works_with": {
        "columns": ["emp_id", "client_id", "total_sales"],
        "labels": ["Employee ID", "Client ID", "Total Sales"]
    }
}

def get_db_connection():
    return mysql.connect(host="localhost", user="root", password=PASSWORD, database=DB_NAME)

def insert():
    current_table = table_var.get()
    values = get_input_values()
    
    if not all(values):
        MessageBox.showinfo("Error", "Please fill all fields")
        return
        
    try:
        con = get_db_connection()
        cursor = con.cursor()
        
        if current_table == "employee":
            values = process_employee_data(values)
        
        columns = TABLE_CONFIGS[current_table]["columns"]
        placeholders = ", ".join(["%s"] * len(columns))
        query = f"INSERT INTO {current_table} ({', '.join(columns)}) VALUES ({placeholders})"
        
        cursor.execute(query, values)
        con.commit()
        clear_entries()
        MessageBox.showinfo("Success", "Record inserted successfully")
        show_table_data()
        
    except mysql.Error as err:
        MessageBox.showerror("Error", f"Database error: {err}")
    finally:
        if 'con' in locals():
            con.close()

def update():
    current_table = table_var.get()
    values = get_input_values()
    
    if not all(values):
        MessageBox.showinfo("Error", "Please fill all fields")
        return
        
    try:
        con = get_db_connection()
        cursor = con.cursor()
        
        if current_table == "employee":
            values = process_employee_data(values)
        
        columns = TABLE_CONFIGS[current_table]["columns"]
        set_clause = ", ".join([f"{col} = %s" for col in columns[1:]])
        query = f"UPDATE {current_table} SET {set_clause} WHERE {columns[0]} = %s"
        
        # Move ID to end for WHERE clause
        values = values[1:] + [values[0]]
        
        cursor.execute(query, values)
        con.commit()
        clear_entries()
        MessageBox.showinfo("Success", "Record updated successfully")
        show_table_data()
        
    except mysql.Error as err:
        MessageBox.showerror("Error", f"Database error: {err}")
    finally:
        if 'con' in locals():
            con.close()

def delete():
    current_table = table_var.get()
    id_value = input_entries[0].get()
    
    if not id_value:
        MessageBox.showinfo("Error", "Please select a record to delete")
        return
        
    try:
        con = get_db_connection()
        cursor = con.cursor()
        
        id_column = TABLE_CONFIGS[current_table]["columns"][0]
        query = f"DELETE FROM {current_table} WHERE {id_column} = %s"
        
        cursor.execute(query, (id_value,))
        con.commit()
        clear_entries()
        MessageBox.showinfo("Success", "Record deleted successfully")
        show_table_data()
        
    except mysql.Error as err:
        MessageBox.showerror("Error", f"Database error: {err}")
    finally:
        if 'con' in locals():
            con.close()

def process_employee_data(values):
    # Handle employee sp aecific data processing
    try:
        # Split full name into first and last name
        full_name = values[1].split()
        if len(full_name) != 2:
            raise ValueError("Please enter both first and last name")
            
        # Format date
        date = datetime.strptime(values[2], '%Y-%m-%d').strftime('%Y-%m-%d')
        
        # Get branch_id from branch_name
        con = get_db_connection()
        cursor = con.cursor()
        cursor.execute("SELECT branch_id FROM branch WHERE branch_name = %s", (values[5],))
        branch_id = cursor.fetchone()
        
        if not branch_id:
            raise ValueError("Invalid branch name")
            
        return [values[0]] + full_name + [date] + [values[3], values[4], branch_id[0]]
        
    except ValueError as e:
        MessageBox.showerror("Error", str(e))
        raise
    finally:
        if 'con' in locals():
            con.close()

def get_input_values():
    return [entry.get() for entry in input_entries]

def clear_entries():
    for entry in input_entries:
        entry.delete(0, END)

def show_table_data():
    current_table = table_var.get()
    
    for row in tree.get_children():
        tree.delete(row)
        
    try:
        con = get_db_connection()
        cursor = con.cursor()
        cursor.execute(f"SELECT * FROM {current_table}")
        rows = cursor.fetchall()
        
        for row in rows:
            tree.insert("", END, values=row)
            
    except mysql.Error as err:
        MessageBox.showerror("Error", f"Database error: {err}")
    finally:
        if 'con' in locals():
            con.close()

def on_table_select(event=None):
    current_table = table_var.get()
    config = TABLE_CONFIGS[current_table]
    
    # Update treeview columns
    tree["columns"] = config["columns"]
    for col in config["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=100)
        
    # Update input fields
    for widget in input_frame.winfo_children():
        widget.destroy()
        
    global input_entries
    input_entries = []
    
    for i, label in enumerate(config["labels"]):
        Label(input_frame, text=label + ":", bg=backgroundcolor, fg="white").grid(row=i, column=0, padx=5, pady=2)
        
        if current_table == "employee" and label == "Branch":
            entry = ttk.Combobox(input_frame)
            fill_branch_dropdown(entry)
        else:
            entry = Entry(input_frame)
        
        entry.grid(row=i, column=1, padx=5, pady=2)
        input_entries.append(entry)
        
    show_table_data()

def fill_branch_dropdown(combobox):
    try:
        con = get_db_connection()
        cursor = con.cursor()
        cursor.execute("SELECT branch_name FROM branch")
        branches = cursor.fetchall()
        combobox['values'] = [branch[0] for branch in branches]
    except mysql.Error as err:
        MessageBox.showerror("Error", f"Database error: {err}")
    finally:
        if 'con' in locals():
            con.close()

def on_tree_select(event):
    selected = tree.selection()
    if not selected:
        return
        
    values = tree.item(selected[0])['values']
    if not values:
        return
        
    # Clear all entries
    clear_entries()
    
    current_table = table_var.get()
    if current_table == "employee":
        # For employee table, special handling for name fields
        e_id = values[0]  # emp_id
        first_name = values[1]  # first_name 
        last_name = values[2]  # last_name
        birth_day = values[3]  # birth_day
        sex = values[4]  # sex
        salary = values[5]  # salary
        branch_id = values[6]  # branch_id
        
        # Get branch name for the branch_id
        try:
            con = get_db_connection()
            cursor = con.cursor()
            cursor.execute("SELECT branch_name FROM branch WHERE branch_id = %s", (branch_id,))
            branch_name = cursor.fetchone()
            if branch_name:
                branch_name = branch_name[0]
        except mysql.Error as err:
            MessageBox.showerror("Error", f"Database error: {err}")
            branch_name = ""
        finally:
            if 'con' in locals():
                con.close()
                
        # Fill in the entries in correct order
        input_entries[0].insert(0, e_id)  # Employee ID
        input_entries[1].insert(0, f"{first_name} {last_name}")  # Full Name
        input_entries[2].insert(0, birth_day)  # Date of Birth
        input_entries[3].insert(0, sex)  # Sex
        input_entries[4].insert(0, salary)  # Salary
        input_entries[5].insert(0, branch_name)  # Branch
        
    else:
        # For other tables, simply fill in the values in order
        for i, value in enumerate(values):
            if value is not None:
                input_entries[i].insert(0, str(value))

# GUI Setup
backgroundcolor = "#06283D"

root = Tk()
root.geometry("800x600")
root.title("Company Database Management")
root.configure(bg=backgroundcolor)

# Table selection
table_var = StringVar(root)
table_var.set("employee")
table_dropdown = ttk.Combobox(root, textvariable=table_var, values=list(TABLE_CONFIGS.keys()))
table_dropdown.place(x=20, y=20)
table_dropdown.bind("<<ComboboxSelected>>", on_table_select)

# Input frame
input_frame = Frame(root, bg=backgroundcolor)
input_frame.place(x=20, y=50, width=400, height=200)

# Buttons
Button(root, text="Insert", command=insert).place(x=20, y=260)
Button(root, text="Update", command=update).place(x=100, y=260)
Button(root, text="Delete", command=delete).place(x=180, y=260)

# Treeview
tree = ttk.Treeview(root)
tree.place(x=20, y=300, width=760, height=280)
tree.bind("<<TreeviewSelect>>", on_tree_select)

# Initialize GUI
on_table_select()

root.mainloop()