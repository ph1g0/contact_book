# -*- coding: utf-8 -*-
"""
Created on Wed May 11 17:14:04 2022

@author: phigo
"""

"""This module provides views to manage the contacts table"""

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from .model import ContactsModel



class Window(QMainWindow):
    """Main Window"""
    def __init__(self, parent=None):       
        """Initializer"""
        super().__init__(parent)
        self.setWindowTitle("Contacts")
        self.resize(1400, 800)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QHBoxLayout()
        self.centralWidget.setLayout(self.layout)
        self.contactsModel = ContactsModel()
        self.setupUI()

    def setupUI(self):
        """Setup the main window's GUI"""
        # Create the table view widget
        self.table = QTableView()
        self.table.setModel(self.contactsModel.model)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.resizeColumnsToContents()

        # Create buttons
        self.addButton = QPushButton("Add...")
        self.addButton.clicked.connect(self.openAddDialog)
        
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.clicked.connect(self.deleteContact)
        
        self.billingAddressToPdfButton = QPushButton("Billing Address to PDF")
        self.billingAddressToPdfButton.clicked.connect(self.billingAddressToPdf)
        
        self.objectAddressToPdfButton = QPushButton("Object Address to PDF")
        self.objectAddressToPdfButton.clicked.connect(self.objectAddressToPdf)
        
        self.clearAllButton = QPushButton("Clear All")
        self.clearAllButton.clicked.connect(self.clearContacts)

        # Lay out the GUI
        layout = QVBoxLayout()
        layout.addWidget(self.addButton)
        layout.addWidget(self.deleteButton)
        layout.addWidget(self.billingAddressToPdfButton)
        layout.addWidget(self.objectAddressToPdfButton)
        layout.addStretch()
        layout.addWidget(self.clearAllButton)
        self.layout.addWidget(self.table)
        self.layout.addLayout(layout)
        
    def openAddDialog(self):
        """Open the Add Contact dialog"""
        dialog = AddDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.contactsModel.addContact(dialog.data)
            self.table.resizeColumnsToContents() 
    
    def deleteContact(self):
        """Delete the selected contact from the database"""
        row = self.table.currentIndex().row()
        if row < 0:
            return

        messageBox = QMessageBox.warning(
            self,
            "Warning!",
            "Do you want to remove the selected contact?",
            QMessageBox.Ok | QMessageBox.Cancel,
        )

        if messageBox == QMessageBox.Ok:
            self.contactsModel.deleteContact(row)
            
    def billingAddressToPdf(self):
        """Export selected contact information to PDF billing address form fields"""
        row = self.table.currentIndex().row()
        if row < 0:
            return
        
        messageBox = QMessageBox.information(
            self,
            "Information!",
            "This exports the selected contact to PDF.\n"
            "This should be used to export the billing address of the contact.\n"
            "The PDF should have form fields with the same name "  
            "as the column headers of the database.\n"
            "For example: 'Name'",
            QMessageBox.Ok | QMessageBox.Cancel,
        )

        if messageBox == QMessageBox.Ok:
            self.contactsModel.billingAddressToPdf(row)
            
    def objectAddressToPdf(self):
        """Export selected contact information to PDF object address form fields"""
        row = self.table.currentIndex().row()
        if row < 0:
            return
        
        messageBox = QMessageBox.information(
            self,
            "Information!",
            "This exports the selected contact to PDF.\n"
            "This should be used to export the object address of the contact.\n"
            "The PDF should have form fields with the same name "  
            "as the column headers of the database but with the prefix 'Object'.\n"
            "For example: 'Object Name'",
            QMessageBox.Ok | QMessageBox.Cancel,
        )

        if messageBox == QMessageBox.Ok:
            self.contactsModel.objectAddressToPdf(row)
            
    def clearContacts(self):
        """Remove all contacts from the database"""
        messageBox = QMessageBox.warning(
            self,
            "Warning!",
            "Do you want to remove all your contacts?",
            QMessageBox.Ok | QMessageBox.Cancel,
        )

        if messageBox == QMessageBox.Ok:
            self.contactsModel.clearContacts()

        
class AddDialog(QDialog):
    """Add Contact dialog"""
    def __init__(self, parent=None):
        """Initializer"""
        super().__init__(parent=parent)
        self.setWindowTitle("Add Contact")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.data = None

        self.setupUI()

    def setupUI(self):
        """Setup the Add Contact dialog's GUI"""
        # Create line edits for data fields
        self.nameField = QLineEdit()
        self.nameField.setObjectName("Name")
        
        self.streetField = QLineEdit()
        self.streetField.setObjectName("Street")
        
        self.cityField = QLineEdit()
        self.cityField.setObjectName("City")
        
        self.phoneField = QLineEdit()
        self.phoneField.setObjectName("Phone")
        
        self.emailField = QLineEdit()
        self.emailField.setObjectName("Email")

        # Lay out the data fields
        layout = QFormLayout()
        layout.addRow("Name:", self.nameField)
        layout.addRow("Street:", self.streetField)
        layout.addRow("City:", self.cityField)
        layout.addRow("Phone:", self.phoneField)
        layout.addRow("Email:", self.emailField)
        self.layout.addLayout(layout)

        # Add standard buttons to the dialog and connect them
        self.buttonsBox = QDialogButtonBox(self)
        self.buttonsBox.setOrientation(Qt.Horizontal)
        self.buttonsBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.buttonsBox.accepted.connect(self.accept)
        self.buttonsBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonsBox)
        
    def accept(self):
        """Accept the data provided through the dialog"""
        self.data = []
        for field in (self.nameField, self.streetField, self.cityField, self.phoneField, self.emailField):
            # This code is to check if all the fields have been filled out 
            # if not field.text():
            #     QMessageBox.critical(
            #         self,
            #         "Error!",
            #         f"You must provide a contact's {field.objectName()}",
            #     )
            #     self.data = None  # Reset .data
            #     return

            self.data.append(field.text())

        if not self.data:
            return

        super().accept()