from tkinter import *
import tkinter.messagebox as MessageBox
import mysql.connector as mysql
from datetime import datetime
from tkinter import ttk

CON = mysql.connect(host="localhost", user="root", password="Ngocchung241120", database="company")
text_boxes = []
labels = []
e_branch = None


def insert():
    global e_branch
    table = e_all_tables.get()
    
    if table == "employee":
        id = text_boxes[0].get()
        name = text_boxes[1].get()
        dob = text_boxes[2].get()
        gender = text_boxes[3].get()
        salary = text_boxes[4].get()
        branch = e_branch.get()
        
        if name == "" or dob == "" or gender == "" or salary == "" or branch == "":
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
            
            if CON.is_connected():
                print("Connected to MySQL Database")
            else:
                print("Not Connected to MySQL Database")
                return
                
            cursor = CON.cursor()
            
            cursor.execute("select branch_id from branch where branch_name = '"+ branch +"'")
            branch_id = cursor.fetchone()
            
            if id == "":
                cursor.execute("insert into employee(first_name, last_name, birth_day, sex, salary, branch_id) values('"+ first_name +"' , '"+ last_name +"', '"+ dob +"', '"+ gender +"', "+ salary +", "+ str(branch_id[0]) +")")
                CON.commit()
            else:
                cursor.execute("insert into employee(emp_id, first_name, last_name, birth_day, sex, salary, branch_id) values("+ id +", '"+ first_name +"' , '"+ last_name +"', '"+ dob +"', '"+ gender +"', "+ salary +", "+ str(branch_id[0]) +")")
                CON.commit()
            
            
            text_boxes[0].delete(0, 'end')
            text_boxes[1].delete(0, 'end')
            text_boxes[2].delete(0, 'end')
            text_boxes[3].delete(0, 'end')
            text_boxes[4].delete(0, 'end')
            
            show(table)
            
            MessageBox.showinfo("Insert Status", "Data was Inserted")
            cursor.close()
            
    elif table == "branch":
        branch_id = text_boxes[0].get()
        branch_name = text_boxes[1].get()
        
        if branch_id == "" or branch_name == "":
            MessageBox.showinfo("Error", "Please fill all the fields")
            return
        else:
            cursor = CON.cursor()
            cursor.execute("insert into branch(branch_id, branch_name) values("+ branch_id +", '"+ branch_name +"')")
            CON.commit()
        
        text_boxes[0].delete(0, 'end')
        text_boxes[1].delete(0, 'end')
        cursor.close()
        
        show(table)
        
        MessageBox.showinfo("Insert Status", "Data was Inserted")
    elif table == "client":
        client_id = text_boxes[0].get()
        client_name = text_boxes[1].get()
        branch = e_branch.get()
        cursor = CON.cursor()
        
        cursor.execute("select branch_id from branch where branch_name = '"+ branch +"'")
        branch_id = cursor.fetchone()
        
        if client_id == "" or client_name == "" or branch == "":
            MessageBox.showinfo("Error", "Please fill all the fields")
            return
        else:
            
            cursor.execute("insert into client(client_id, client_name, branch_id) values("+ client_id +", '"+ client_name +"', "+ str(branch_id[0]) +")")
            CON.commit()
        
        text_boxes[0].delete(0, 'end')
        text_boxes[1].delete(0, 'end')
        cursor.close()
        show(table)
        MessageBox.showinfo("Insert Status", "Data was Inserted")
    elif table == "works_with":
        emp_id = text_boxes[0].get()
        client_id = text_boxes[1].get()
        total_sales = text_boxes[2].get()
        
        cursor = CON.cursor()
        
        
        
        if emp_id == "" or client_id == "" or total_sales == "":
            MessageBox.showinfo("Error", "Please fill all the fields")
            return
        else:
            cursor.execute("select emp_id from employee where emp_id = "+ emp_id +"")
            emp_id = cursor.fetchone()
            
            cursor.execute("select client_id from client where client_id = "+ client_id +"")
            client_id = cursor.fetchone()
            
            if emp_id == None:
                MessageBox.showinfo("Error", "Employee ID does not exist")
                return
            elif client_id == None:
                MessageBox.showinfo("Error", "Client ID does not exist")
                return
            
            cursor.execute("insert into works_with(emp_id, client_id, total_sales) values("+ str(emp_id[0]) +", "+ str(client_id[0]) +", "+ total_sales +")")
            CON.commit()
        
        text_boxes[0].delete(0, 'end')
        text_boxes[1].delete(0, 'end')
        text_boxes[2].delete(0, 'end')
        cursor.close()
        show(table)
        MessageBox.showinfo("Insert Status", "Data was Inserted")
        
        
        
        
    

def delete():
    table = e_all_tables.get()
    
    if table == "employee":
        id = text_boxes[0].get()
        if(id == ""):
            MessageBox.showinfo("Error", "Please enter the id of the employee to delete")
            return
        else:
        
            if CON.is_connected():
                print("Connected to MySQL Database")
            else:
                print("Not Connected to MySQL Database")
                return
            
            cursor = CON.cursor()
        
            cursor.execute(f"select * from employee where emp_id = {id}")
            result = cursor.fetchone()
        
            if result == None:
                MessageBox.showinfo("Error", "Employee ID not found")
            else:
                cursor.execute(f"delete from employee where emp_id = {id}")
                CON.commit()
        
                text_boxes[0].delete(0, 'end')
            
                show(table)
            
                MessageBox.showinfo("Delete Status", "Data was Deleted")
            cursor.close()
    elif table == "branch":
        branch_id = text_boxes[0].get()
        
        if(branch_id == ""):
            MessageBox.showinfo("Error", "Please enter the branch id to delete")
            return
        else:
            cursor = CON.cursor()
            
            cursor.execute(f"select * from branch where branch_id = {branch_id}")
            result = cursor.fetchone()
            
            if result == None:
                MessageBox.showinfo("Error", "Branch ID not found")
            else:
                cursor.execute(f"delete from branch where branch_id = {branch_id}")
                CON.commit()
        
                text_boxes[0].delete(0, 'end')
            
                show(table)
            
                MessageBox.showinfo("Delete Status", "Data was Deleted")
            cursor.close()
    elif table == "client":
        client_id = text_boxes[0].get()
        
        if(client_id == ""):
            MessageBox.showinfo("Error", "Please enter the client id to delete")
            return
        else:
            cursor = CON.cursor()
            
            cursor.execute(f"select * from client where client_id = {client_id}")
            result = cursor.fetchone()
            
            if result == None:
                MessageBox.showinfo("Error", "Client ID not found")
            else:
                cursor.execute(f"delete from client where client_id = {client_id}")
                CON.commit()
        
                text_boxes[0].delete(0, 'end')
            
                show(table)
            
                MessageBox.showinfo("Delete Status", "Data was Deleted")
            cursor.close()
    elif table == "works_with":
        emp_id = text_boxes[0].get()
        client_id = text_boxes[1].get()
        
        if emp_id == "" or client_id == "":
            MessageBox.showinfo("Error", "Please enter a employee and client id to delete")
            return
        else:
            cursor = CON.cursor()
            
            cursor.execute(f"select * from works_with where emp_id = {emp_id} and client_id = {client_id}")
            result = cursor.fetchone()
            
            if result == None:
                MessageBox.showinfo("Error", "Entry not found")
                return
            else:
                cursor.execute(f"delete from works_with where emp_id = {str(emp_id)} and client_id = {str(client_id)}")
                CON.commit()
            
                
                
                
        text_boxes[0].delete(0, 'end')
        text_boxes[1].delete(0, 'end')
            
        show(table)
            
        MessageBox.showinfo("Delete Status", "Data was Deleted")
        cursor.close()
            
            


def update():
    global e_branch
    table = e_all_tables.get()
    
    if table == "employee":
        id = text_boxes[0].get()
        name = text_boxes[1].get()
        dob = text_boxes[2].get()
        gender = text_boxes[3].get()
        salary = text_boxes[4].get()
        branch = e_branch.get()
        
        if id == "" or name == "" or dob == "" or gender == "" or salary == "" or branch == "":
            MessageBox.showinfo("Error", "Please fill all the fields")
            return
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
            MessageBox.showinfo("Error", "Date of birth must be formatted as MM/DD/YYYY")
            return
        
        
        if CON.is_connected():
            print("Connected to MySQL Database")
        else:
            print("Not Connected to MySQL Database")
            return
        cursor = CON.cursor()
        
        cursor.execute("select branch_id from branch where branch_name = '"+ branch +"'")
        branch_id = cursor.fetchone()
        
        if branch_id == None:
            MessageBox.showinfo("Error", "Branch does not exist")
            return
        
        cursor.execute(f"""
                UPDATE employee
                SET first_name = '{first_name}', last_name = '{last_name}', birth_day = '{dob}', sex = '{gender}', salary = {salary}, branch_id = {str(branch_id[0])}
                WHERE emp_id = {id}
            """)
        CON.commit()
        text_boxes[0].delete(0, 'end')
        text_boxes[1].delete(0, 'end')
        text_boxes[2].delete(0, 'end')
        text_boxes[3].delete(0, 'end')
        text_boxes[4].delete(0, 'end')

        show(table)
        
        MessageBox.showinfo("Update Status", "Data was Updated")
        cursor.close()
    elif table == "branch":
        branch_id = text_boxes[0].get()
        branch_name = text_boxes[1].get()
        
        if branch_id == "" or branch_name == "":
            MessageBox.showinfo("Error", "Please fill all the fields")
            return
        else:
            cursor = CON.cursor()
        
            cursor.execute("select branch_id from branch where branch_id = "+ branch_id +"")
            result = cursor.fetchone()
            
            if result == None:
                MessageBox.showinfo("Error", "Branch does not exist")
                return
            
            cursor.execute(f"""
                    UPDATE branch
                    SET branch_name = '{branch_name}'
                    WHERE branch_id = {branch_id}
                """)
            CON.commit()
            text_boxes[0].delete(0, 'end')
            text_boxes[1].delete(0, 'end')

            show(table)
            
            MessageBox.showinfo("Update Status", "Data was Updated")
            cursor.close()
    elif table == "client":
        client_id = text_boxes[0].get()
        client_name = text_boxes[1].get()
        branch_name = e_branch.get()
        
        if client_id == "" or client_name == "" or branch_name == "":
            MessageBox.showinfo("Error", "Please fill all the fields")
            return
        else:
            cursor = CON.cursor()
        
            cursor.execute("select branch_id from branch where branch_name = '"+ branch_name +"'")
            branch_id = cursor.fetchone()
            
            cursor.execute("select client_id from client where client_id = "+ client_id +"")
            result = cursor.fetchone()
            
            if branch_id == None:
                MessageBox.showinfo("Error", "Branch does not exist")
                return
            elif result == None:
                MessageBox.showinfo("Error", "Client does not exist")
                return
            
            cursor.execute(f"""
                    UPDATE client
                    SET client_name = '{client_name}', branch_id = {str(branch_id[0])}
                    WHERE client_id = {client_id}
                """)
            CON.commit()
            text_boxes[0].delete(0, 'end')
            text_boxes[1].delete(0, 'end')

            show(table)
            
            MessageBox.showinfo("Update Status", "Data was Updated")
            cursor.close()
    elif table == "works_with":
        emp_id = text_boxes[0].get()
        client_id = text_boxes[1].get()
        total_sales = text_boxes[2].get()
        
        if emp_id == "" or client_id == "":
            MessageBox.showinfo("Error", "Please enter an employee and client id")
            return
        elif total_sales == "":
            MessageBox.showinfo("Error", "Please enter total sales")
            return
        else:
            cursor = CON.cursor()
            
            cursor.execute(f"select * from works_with where emp_id = {emp_id} and client_id = {client_id}")
            result = cursor.fetchone()
            
            if result == None:
                MessageBox.showinfo("Error", "Entry not found")
                return
            else:
                
                cursor.execute(f"""
                    UPDATE works_with
                    SET total_sales = {total_sales}
                    WHERE emp_id = {emp_id} and client_id = {client_id}
                """)
                CON.commit()

            text_boxes[0].delete(0, 'end')
            text_boxes[1].delete(0, 'end')
            text_boxes[2].delete(0, 'end')

            show(table)
            
            MessageBox.showinfo("Update Status", "Data was Updated")
            cursor.close()
        
        
        

def show(table):
    for row in tree.get_children():
        tree.delete(row)
    
    cursor = CON.cursor()
    cursor.execute("SELECT * FROM "+ table +"")
    rows = cursor.fetchall()
    
    for row in rows:
        tree.insert("", "end", values=row)

def fill_combo_box():
    global e_branch
    cursor = CON.cursor()
    cursor.execute("select branch_name from branch")
    branches = cursor.fetchall()
    cursor.close()
    
    e_branch['values'] = [f"{values[0]}" for values in branches]

def create_text_boxes(event=None):
    global e_branch
    clear_text_boxes_and_labels()  
    
    selected_table = e_all_tables.get()

    if selected_table == "employee":  
        field_labels = ["Enter Employee ID:", "Enter Name:", "Enter Date of Birth:", "Enter Sex:", "Enter Salary:", "Enter Branch:"]
        header.config(text="Employee Info")
        for i, label_text in enumerate(field_labels):
            label = Label(root, text=label_text, font=("bold", 10), bg=backgroundcolor, fg="white")
            label.place(x=20, y=60 + (i * 25))  
            entry = Entry(root)
            entry.place(x=170, y=60 + (i * 25))  
            text_boxes.append(entry)  
            labels.append(label)  
        e_branch = ttk.Combobox(root)
        e_branch.place(x=170, y=185)
        fill_combo_box()
    elif selected_table == "branch":
        field_labels = ["Enter Branch ID:", "Enter Branch Name:"]
        header.config(text="Branch")
        for i, label_text in enumerate(field_labels):
            label = Label(root, text=label_text, font=("bold", 10), bg=backgroundcolor, fg="white")
            label.place(x=20, y=60 + (i * 25))  
            entry = Entry(root)
            entry.place(x=170, y=60 + (i * 25))  
            text_boxes.append(entry)  
            labels.append(label)
    elif selected_table == "client":
        field_labels = ["Enter Client ID:", "Enter Client Name:", "Enter Branch:"]
        header.config(text="Client")
        for i, label_text in enumerate(field_labels):
            label = Label(root, text=label_text, font=("bold", 10), bg=backgroundcolor, fg="white")
            label.place(x=20, y=60 + (i * 25))  
            entry = Entry(root)
            entry.place(x=170, y=60 + (i * 25))  
            text_boxes.append(entry)  
            labels.append(label)  
        e_branch = ttk.Combobox(root)
        e_branch.place(x=170, y=110)
        fill_combo_box()
    elif selected_table == "works_with":
        field_labels = ["Enter Employee ID:", "Enter Client ID:", "Enter Total Sales:"]
        header.config(text="Works With")
        for i, label_text in enumerate(field_labels):
            label = Label(root, text=label_text, font=("bold", 10), bg=backgroundcolor, fg="white")
            label.place(x=20, y=60 + (i * 25))  
            entry = Entry(root)
            entry.place(x=170, y=60 + (i * 25))  
            text_boxes.append(entry)  
            labels.append(label)  

def on_table_select(event=None):
    selected_table = e_all_tables.get()
    if selected_table == "employee":
        columns = ("emp_id", "first_name", "last_name", "birth_day", "sex", "salary", "branch_id")
    elif selected_table == "branch":
        columns = ("branch_id", "branch_name")
    elif selected_table == "client":
        columns = ("client_id", "client_name", "branch_id")
    elif selected_table == "works_with":
        columns = ("emp_id", "client_id", "total_sales")
    else:
        return

    tree["columns"] = columns
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    show_table_data(selected_table)
    
    create_text_boxes()

def show_table_data(table_name):
    for row in tree.get_children():
        tree.delete(row)
    
    cursor = CON.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    
    for row in rows:
        tree.insert("", "end", values=row)

def clear_text_boxes_and_labels():
    global e_branch
    if len(text_boxes) != 0 and len(labels) != 0:
        for text_box in text_boxes:
            text_box.destroy()  
        for label in labels:
            label.destroy()  
    if e_branch != None:
        e_branch.destroy()
        e_branch = None
    text_boxes.clear()  
    labels.clear()  
    e_branch = None
    
def tree_select(event):
    cursor = CON.cursor()
    
    item = tree.selection()
    
    if item:
        values = tree.item(item, "values")
        
        table = e_all_tables.get()
        
        if table == "employee":
            text_boxes[0].delete(0, 'end')
            text_boxes[1].delete(0, 'end')
            text_boxes[2].delete(0, 'end')
            text_boxes[3].delete(0, 'end')
            text_boxes[4].delete(0, 'end')
            e_branch.delete(0,'end')
        
            text_boxes[0].insert(0, values[0])  
            text_boxes[1].insert(0, values[1] + " " + values[2])  
            text_boxes[2].insert(0, datetime.strptime(values[3], '%Y-%m-%d').strftime('%m/%d/%Y'))  
            text_boxes[3].insert(0, values[4])  
            text_boxes[4].insert(0, values[5])  
            
            cursor.execute("select branch_name from branch where branch_id = "+ values[6] +"")
            branch_name = cursor.fetchone()[0]
            e_branch.set(branch_name)  
        elif table == "branch":
            text_boxes[0].delete(0, 'end')
            text_boxes[1].delete(0, 'end')
            
            text_boxes[0].insert(0, values[0])
            text_boxes[1].insert(0, values[1])
        elif table == "client":
            text_boxes[0].delete(0, 'end')
            text_boxes[1].delete(0, 'end')
            e_branch.delete(0,'end')
            
            text_boxes[0].insert(0, values[0])
            text_boxes[1].insert(0, values[1])
            cursor.execute("select branch_name from branch where branch_id = "+ values[2] +"")
            branch_name = cursor.fetchone()[0]
            e_branch.set(branch_name)
        elif table == "works_with":
            text_boxes[0].delete(0, 'end')
            text_boxes[1].delete(0, 'end')
            text_boxes[2].delete(0, 'end')
            
            text_boxes[0].insert(0, values[0])
            text_boxes[1].insert(0, values[1])
            text_boxes[2].insert(0, values[2])



backgroundcolor = "#06283D"

root = Tk()
root.geometry("800x600")
root.title("Employee Information System")
root.config(bg=backgroundcolor)

header = Label(root, text="Employee Info", font=("bold", 12), bg=backgroundcolor, fg="white")
header.place(x=125, y=30)





# Dropdown menu for all tables
tables = ["employee", "branch", "client", "works_with"]
e_all_tables = ttk.Combobox(root, values=tables)
e_all_tables.current(0)


e_all_tables.place(x=350, y=225)
e_all_tables.bind("<<ComboboxSelected>>", on_table_select)


insert_data = Button(root, text="Insert", font=("italic", 10), bg="white", command=insert)
insert_data.place(x=20, y= 210)

delete_data = Button(root, text="Delete", font=("italic", 10), bg="white", command=delete)
delete_data.place(x=70, y= 210)

update_data = Button(root, text="Update", font=("italic", 10), bg="white", command=update)
update_data.place(x=125, y= 210)


columns = ("emp_id", "first_name", "last_name", "birth_day", "sex", "salary", "branch_id")
tree = ttk.Treeview(root, columns=columns, show="headings")
on_table_select()
tree.bind("<<TreeviewSelect>>", tree_select)
tree.heading("emp_id", text="emp_id")
tree.heading("first_name", text="first_name")
tree.heading("last_name", text="last_name")
tree.heading("birth_day", text="birth_date")
tree.heading("sex", text="sex")
tree.heading("salary", text="salary")
tree.heading("branch_id", text="branch_id")

tree.column("emp_id", width=50)
tree.column("first_name", width=70)
tree.column("last_name", width=70)
tree.column("birth_day", width=100)
tree.column("sex", width=50)
tree.column("salary", width=80)
tree.column("branch_id", width=50)

tree.place(x=20, y=270, width=760, height=310)

show("employee")

root.mainloop()

CON.close()