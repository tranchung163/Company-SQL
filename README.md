# Employee Information System

A desktop application built with Python and Tkinter that provides a user-friendly interface for managing employee records in a MySQL database. This application allows users to perform CRUD (Create, Read, Update, Delete) operations on employee data.

## Features

- Add new employee records with validation
- View all employee records in a tabular format
- Update existing employee information
- Delete employee records
- Interactive data table with click-to-fill functionality
- Input validation for all fields
- Clean and intuitive user interface

## Prerequisites

Before running this application, make sure you have the following installed:

- Python 3.x
- MySQL Server
- Required Python packages:
  ```
  mysql-connector-python
  pymysql
  tkinter (usually comes with Python)
  ```

## Database Setup

1. Install MySQL Server on your system
2. Create a new database named `company`
3. Create the `employee` table with the following structure:
   ```sql
   CREATE TABLE employee (
       emp_id INT PRIMARY KEY,
       first_name VARCHAR(50),
       last_name VARCHAR(50),
       birth_day DATE,
       sex VARCHAR(10),
       salary DECIMAL(10,2)
   );
   ```

## Installation

1. Clone this repository:

   ```bash
   git clone [repository-url]
   ```

2. Install the required Python packages:

   ```bash
   pip install mysql-connector-python pymysql
   ```

3. Update the database connection parameters in the code:
   ```python
   host="localhost"
   user="root"
   password="your_password"
   database="company"
   ```

## Usage

1. Run the application:

   ```bash
   python employee_system.py
   ```

2. The application window will open with the following features:
   - Input fields for employee information
   - Action buttons (Insert, Delete, Update)
   - Data table showing all employee records

### Adding a New Employee

- Fill in all fields (Employee ID, Name, Date of Birth, Sex, Salary)
- Name should be entered as "First Last"
- Date format should be MM/DD/YYYY
- Click "Insert" button

### Updating an Employee

- Click on an employee record in the table
- Fields will automatically populate with the selected employee's data
- Modify the desired fields
- Click "Update" button

### Deleting an Employee

- Enter the Employee ID or select the employee from the table
- Click "Delete" button

## Input Validation

The application includes validation for:

- Empty fields
- Proper name format (First Last)
- Date format (MM/DD/YYYY)
- Employee ID existence for updates and deletions

## Technical Details

- Built with Python's Tkinter library for GUI
- Uses MySQL for database operations
- Implements error handling for database operations
- Features a responsive treeview for data display
- Uses parameterized queries to prevent SQL injection

## Color Scheme

- Background Color: #06283D
- Text Color: White
- Buttons: White background with black text

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

[Your chosen license]

## Author

Ngoc
Joe
