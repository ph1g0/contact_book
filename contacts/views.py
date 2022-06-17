# -*- coding: utf-8 -*-
"""
Created on Wed May 11 17:14:04 2022

@author: ph1g0
"""

"""This module provides views to manage the contacts table"""

from pathlib import Path

from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from .model import ContactsModel

from ext.offer_number import readOfferNumber



class Window(QMainWindow):
    """Main Window"""
    def __init__(self, parent=None):       
        """Initializer"""
        super().__init__(parent)
        self.setWindowTitle("Contacts")
        self.resize(1600, 800)
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
        self.table.setSortingEnabled(True)
        self.table.sortByColumn(0, Qt.AscendingOrder)
        self.table.verticalHeader().setVisible(False)
        
        # Setup Proxy Model
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setFilterKeyColumn(-1) # Search all columns.
        self.proxy_model.setSourceModel(self.contactsModel.model)
        self.proxy_model.sort(0, Qt.AscendingOrder)
        self.table.setModel(self.proxy_model)
        
        # Create search bar
        self.searchbar = QLineEdit()
        self.searchbar.textChanged.connect(self.proxy_model.setFilterFixedString)
        
        # Create label for offer number
        offer_number = readOfferNumber()
        self.offerNumber = QLabel()
        self.offerNumber.setText("Offer: %s" %offer_number)
        self.offerNumber.setToolTip(
            "To change the offer number, open offer_number.txt\n"
            "Offer number is only updated after restart of the application."
            )

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
        
        layout.addWidget(self.searchbar)
        self.searchbar.setPlaceholderText("Search...")
        self.searchbar.setFixedWidth(200)
        
        layout.addWidget(self.offerNumber)
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
        # Get the row of the selected contact
        # mapToSource() maps the selected contact index back to the orignal model
        row = self.proxy_model.mapToSource(self.table.currentIndex()).row()
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
        # Get the row of the selected contact
        # mapToSource() maps the selected contact index back to the orignal model
        row = self.proxy_model.mapToSource(self.table.currentIndex()).row()
        if row < 0:
            return
        
        messageBox = QMessageBox.information(
            self,
            "Information!",
            "This exports the selected contact to PDF.\n"
            "This should be used to export the billing address of the contact.\n"
            "It also adds the offer number to the PDF (form field 'Offer').\n"
            "The PDF should have form fields with the same name "  
            "as the column headers of the database.\n"
            "For example: 'Name1'",
            QMessageBox.Ok | QMessageBox.Cancel,
        )

        if messageBox == QMessageBox.Ok:
            # Select input PDF file
            input_pdf = self.fileDialog()
            
            # Call billingAddressToPdf function 
            self.contactsModel.billingAddressToPdf(row, input_pdf[0])
            
        # Update offer number label
        offer_number = readOfferNumber()
        self.offerNumber.setText("Offer: %s" %offer_number)
            
    def objectAddressToPdf(self):
        """Export selected contact information to PDF object address form fields"""
        # Get the row of the selected contact
        # mapToSource() maps the selected contact index back to the orignal model
        row = self.proxy_model.mapToSource(self.table.currentIndex()).row()
        if row < 0:
            return
        
        messageBox = QMessageBox.information(
            self,
            "Information!",
            "This exports the selected contact to PDF.\n"
            "This should be used to export the object address of the contact.\n"
            "The PDF should have form fields with the same name "  
            "as the column headers of the database but with the prefix 'Object'.\n"
            "For example: 'Object Name1'",
            QMessageBox.Ok | QMessageBox.Cancel,
        )

        if messageBox == QMessageBox.Ok:
            # Select input PDF file
            input_pdf = self.fileDialog()
            
            # Call objectAddressToPdf function 
            self.contactsModel.objectAddressToPdf(row, input_pdf[0])
            
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
            
    def fileDialog(self):
        home_dir = str(Path.home())
        input_pdf = QFileDialog.getOpenFileName(self, 'Open file', home_dir)
        
        return input_pdf

        
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
        self.name1Field = QLineEdit()
        self.name1Field.setObjectName("Name1")
        
        self.name2Field = QLineEdit()
        self.name2Field.setObjectName("Name2")
        
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
        layout.addRow("Name1:", self.name1Field)
        layout.addRow("Name2:", self.name2Field)
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
        for field in (
                self.name1Field, 
                self.name2Field, 
                self.streetField, 
                self.cityField, 
                self.phoneField, 
                self.emailField):
            self.data.append(field.text())

        if not self.data:
            return

        super().accept()