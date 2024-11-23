from tkinter import *
import tkinter.messagebox as MessageBox
import mysql.connector as mysql
import pymysql
from datetime import datetime
from tkinter import ttk

def insert():
    id = e_id.get()
    name = e_name.get()
    dob = e_DOB.get()
    gender = e_gender.get()
    salary = e_salary.get()
    
    if id == "" or name == "" or dob == "" or gender == "" or salary == "" :
        MessageBox.showinfo("Error", "Please fill all the fields")
    else:
        names = name.split()
        if len(names) == 2:
            first_name = names[0]
            last_name = names[1]
        else:
            MessageBox.showinfo("Error", "Enter First and Last Name")
            return
    
        try:
            dob = datetime.strptime(dob, '%m/%d/%Y').strftime('%Y-%m-%d')
        except ValueError:
            MessageBox.showinfo("Error", "Date of birth must be formated as MM/DD/YYYY")
            return
    
        con = mysql.connect(host="localhost", user="root", password="Ngocchung241120", database="company")
        
        if con.is_connected():
            print("Connected to MySQL Database")
        else:
            print("Not Connected to MySQL Database")
            return
            
        cursor = con.cursor()
        cursor.execute("insert into employee(emp_id, first_name, last_name, birth_day, sex, salary) values("+ id +", '"+ first_name +"' , '"+ last_name +"', '"+ dob +"', '"+ gender +"', "+ salary +")")
        con.commit()
        
        e_id.delete(0, 'end')
        e_name.delete(0, 'end')
        e_DOB.delete(0, 'end')
        e_gender.delete(0, 'end')
        e_salary.delete(0, 'end')
        
        MessageBox.showinfo("Insert Status", "Data was Inserted")
        cursor.close()
        show()

def delete():
    if(e_id.get() == ""):
        MessageBox.showinfo("Error", "Please enter the id of the employee to delete")
    else:
        con = mysql.connect(host="localhost", user="root", password="Ngocchung241120", database="company")
        
        if con.is_connected():
            print("Connected to MySQL Database")
        else:
            print("Not Connected to MySQL Database")
            return
            
        cursor = con.cursor()
        
        cursor.execute(f"select * from employee where emp_id = {e_id.get()}")
        result = cursor.fetchone()
        
        if result == None:
            MessageBox.showinfo("Error", "Employee ID not found")
        else:
            cursor.execute(f"delete from employee where emp_id = {e_id.get()}")
            con.commit()
        
            e_id.delete(0, 'end')
            e_name.delete(0, 'end')
            e_DOB.delete(0, 'end')
            e_gender.delete(0, 'end')
            e_salary.delete(0, 'end')
        
            MessageBox.showinfo("Delete Status", "Data was Deleted")
            cursor.close()
            show()
        
        

def fill_data(event):
    # Clear all entries first
    e_id.delete(0, 'end')
    e_name.delete(0, 'end')
    e_DOB.delete(0, 'end')
    e_gender.delete(0, 'end')
    e_salary.delete(0, 'end')
    
    # Get selected item
    selected_item = tree.selection()[0]
    values = tree.item(selected_item)['values']
    
    # Fill the entries with selected data
    e_id.insert(0, values[0])
    e_name.insert(0, f"{values[1]} {values[2]}")  # Combine first and last name
    e_DOB.insert(0, datetime.strptime(str(values[3]), '%Y-%m-%d').strftime('%m/%d/%Y'))  # Convert date format
    e_gender.insert(0, values[4])
    e_salary.insert(0, values[5])

def update():
    id = e_id.get()
    name = e_name.get()
    dob = e_DOB.get()
    gender = e_gender.get()
    salary = e_salary.get()
    
    if id == "" or name == "" or dob == "" or gender == "" or salary == "":
        MessageBox.showinfo("Error", "Please fill all the fields")
        return
        
    names = name.split()
    if len(names) == 2:
        first_name = names[0]
        last_name = names[1]
    else:
        MessageBox.showinfo("Error", "Enter First and Last Name")
        return
    
    try:
        dob = datetime.strptime(dob, '%m/%d/%Y').strftime('%Y-%m-%d')
    except ValueError:
        MessageBox.showinfo("Error", "Date of birth must be formatted as MM/DD/YYYY")
        return
    
    try:
        con = mysql.connect(host="localhost", user="root", password="Ngocchung241120", database="company")
        if con.is_connected():
            print("Connected to MySQL Database")
        else:
            print("Not Connected to MySQL Database")
            return
            
        cursor = con.cursor()
        
        # First check if employee exists
        cursor.execute(f"SELECT * FROM employee WHERE emp_id = {id}")
        if cursor.fetchone() is None:
            MessageBox.showinfo("Error", "Employee ID not found")
            return
            
        # Update the employee data
        cursor.execute("""
            UPDATE employee 
            SET first_name = %s, 
                last_name = %s, 
                birth_day = %s, 
                sex = %s, 
                salary = %s 
            WHERE emp_id = %s
        """, (first_name, last_name, dob, gender, salary, id))
        
        con.commit()
        
        # Clear all fields
        e_id.delete(0, 'end')
        e_name.delete(0, 'end')
        e_DOB.delete(0, 'end')
        e_gender.delete(0, 'end')
        e_salary.delete(0, 'end')
        
        MessageBox.showinfo("Update Status", "Data was Updated Successfully")
        show()  # Refresh the treeview
        
    except mysql.Error as err:
        MessageBox.showinfo("Error", f"An error occurred: {err}")
        
    finally:
        if 'con' in locals() and con.is_connected():
            cursor.close()
            con.close()
            print("MySQL connection is closed")

def show():
    for row in tree.get_children():
        tree.delete(row)
    
    con = mysql.connect(host="localhost", user="root", password="Ngocchung241120", database="company")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM employee")
    rows = cursor.fetchall()
    
    for row in rows:
        tree.insert("", "end", values=row)
    con.close()
    
        


backgroundcolor = "#06283D"

root = Tk()
root.geometry("470x400")
root.title("Employee Information System")
root.config(bg=backgroundcolor)
root.resizable(False, False)

header = Label(root, text="Employee Info", font=("bold", 12), bg=backgroundcolor, fg="white")
header.place(x=125, y=30)

id = Label(root, text="Enter Employee ID:", font=("bold", 10), bg=backgroundcolor, fg="white")
id.place(x=20, y=60)


e_id = Entry(root)
e_id.place(x=170, y=60)


name = Label(root, text="Enter Name:", font=("bold", 10), bg=backgroundcolor, fg="white")
name.place(x=20, y=85)

e_name = Entry(root)
e_name.place(x=170, y=85)

dob = Label(root, text="Enter Date of Birth:", font=("bold", 10), bg=backgroundcolor, fg="white")
dob.place(x=20, y=110)

e_DOB = Entry(root)
e_DOB.place(x=170, y=110)

gender = Label(root, text="Enter Sex:", font=("bold", 10), bg=backgroundcolor, fg="white")
gender.place(x=20, y=135)

e_gender = Entry(root)
e_gender.place(x=170, y=135)

salary = Label(root, text="Enter Salary:", font=("bold", 10), bg=backgroundcolor, fg="white")
salary.place(x=20, y=160)

e_salary = Entry(root)
e_salary.place(x=170, y=160)

insert_data = Button(root, text="Insert", font=("italic", 10), bg="white", command=insert)
insert_data.place(x=20, y= 185)

delete_data = Button(root, text="Delete", font=("italic", 10), bg="white", command=delete)
delete_data.place(x=70, y= 185)

update_data = Button(root, text="Update", font=("italic", 10), bg="white", command=update)
update_data.place(x=125, y= 185)

get = Button(root, text="Get", font=("italic", 10), bg="white")
get.place(x=185, y= 185)

columns = ("emp_id", "first_name", "last_name", "birth_day", "sex", "salary")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("emp_id", text="emp_id")
tree.heading("first_name", text="first_name")
tree.heading("last_name", text="last_name")
tree.heading("birth_day", text="birth_date")
tree.heading("sex", text="sex")
tree.heading("salary", text="salary")

tree.column("emp_id", width=50)
tree.column("first_name", width=70)
tree.column("last_name", width=70)
tree.column("birth_day", width=100)
tree.column("sex", width=50)
tree.column("salary", width=80)

tree.place(x=20, y=220, width=430, height=150)

tree.place(x=20, y=220, width=430, height=150)
tree.bind('<<TreeviewSelect>>', fill_data)


root.mainloop()