# -*- coding: utf-8 -*-
# contacts/main.py
"""
Created on Wed May 11 17:24:15 2022

@author: phigo
"""

"""This module provides Contacts application"""

import sys

from PySide2.QtWidgets import QApplication

from .database import createConnection
from .views import Window

def main():
    """Contacts main function"""
    # Create the application
    app = QApplication(sys.argv)
    
    # Connect to the database before creating any window
    if not createConnection("contacts.sqlite"):
        sys.exit(1)

    # Create the main window
    win = Window()
    win.show()
    
    # Run the event loop
    sys.exit(app.exec_())