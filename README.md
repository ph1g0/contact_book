# contact_book
SQLlite database for storing contact data and exporting contact data to PDF form fields.   
The PDF form fields have to have the same name as the columns in the database.
![grafik](https://user-images.githubusercontent.com/105172511/172037614-53947a83-4834-4d3f-b0b7-609cc3744b96.png)

You can either choose to export a contact as billing address or object address.
![grafik](https://user-images.githubusercontent.com/105172511/172037698-f8574f82-8a91-403d-b323-12f543aefc77.png)


# Running the Application
To run Contacts, you need to download the source code. Then open a terminal or command-line window and run the following steps:
1. Create and activate a Python virtual environment  
  ```
  $ cd contacts/
  $ python -m venv ./venv
  $ venv\Scripts\activate.bat
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
 - 0.3.0 Export to PDF form fields implemented
 - 1.0.0 First release

# About the Author
ph1g0

# License
Distributed under the MIT license.
