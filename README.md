Malaysian Tax Input Program (SQITK3073 Individual Project)

This project is a Python program developed for the SQITK3073 Business Analytic Programming course.
It allows users to register using their IC number, authenticate, calculate tax payable, and store data in a CSV file.

📌 Objectives

Implement user registration and login using IC number

Calculate Malaysian individual tax payable

Apply tax relief values

Store and retrieve data from CSV using pandas

Demonstrate Python programming concepts (loops, functions, lists, sets, dictionaries)

📌 Features

✔ User Registration
✔ IC Number Authentication (last 4 digits as password)
✔ Annual Income Input
✔ Tax Relief Input
✔ Automatic Tax Calculation
✔ Save User Data to CSV
✔ Read and Display Tax Records

📌 How to Run the Program
1. Install Python (3.8+)

Download from python.org

2. Install required library
pip install pandas

3. Run the program
python main.py

📌 File Descriptions
File	Description
main.py	Main program: registration, login, input, display, workflow
functions.py	Contains verify_user(), calculate_tax(), save_to_csv(), read_from_csv()
tax_data.csv	Stores IC, income, tax relief, tax payable (created automatically)
README.md	Project documentation
📌 Libraries Used
pandas

📌 Sample Program Flow

User registers (IC + password = last 4 digits)

Program verifies user

User enters income + tax relief

Program calculates tax payable

Data saved to CSV

User can view all saved records

📌 GitHub Source Code

(https://github.com/nurulumairahbatrisyia-gif/malaysian-tax-input-program.git)

📌 Author

Name: Nurul Umairah Batrisyia Binti Mohd Syafarudy
Course: SQITK3073 Business Analytic Programming
