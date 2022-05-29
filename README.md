# contact_book
SQLlite database for storing contact data and exporting contact data to PDF form fields.   
The PDF form fields have to have the same name as the columns in the database. 
![grafik](https://user-images.githubusercontent.com/105172511/170858044-dc8e4595-e918-4d9e-a11f-7c05b654810f.png)

Export to PDF:
![grafik](https://user-images.githubusercontent.com/105172511/170858114-449cc0f4-53d7-40cb-a46d-eb8cd63a422d.png)

# Running the Application
To run Contacts, you need to download the source code. Then open a terminal or command-line window and run the following steps:
1. Create and activate a Python virtual environment  
  ```
  $ cd contacts/
  $ python -m venv ./venv
  $ source venv/bin/activate
  (venv)$
  ```

2. Install the dependencies  
  ```
  (venv) $ python -m pip install -r requirements.txt
  ```
  
3. Run the application  
  ```
  (venv) $ python contacts.py
  ```
  
Note: This application was coded and tested using Python 3.9.12, PyQt 5.9.2 and pdfrw 0.4.

# Release History
 - 0.1.0 A work in progress (Example from Real Python) -> https://realpython.com/python-contact-book/  
 - 0.2.0 Added new colums for contact information and resized window
 - 1.0.0 Export to PDF form fields implemented

# About the Author
ph1g0

# License
Distributed under the MIT license.
