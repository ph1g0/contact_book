# -*- coding: utf-8 -*-
"""
Created on Sat May 14 17:15:57 2022

@author: phigo
"""

"""This module provides a model to manage the contacts table"""

from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel
from pdf.modify_pdf import fill_pdf



class ContactsModel:
    def __init__(self):
        self.model = self._createModel()

    @staticmethod
    def _createModel():
        """Create and set up the model"""
        tableModel = QSqlTableModel()
        tableModel.setTable("contacts")
        tableModel.setEditStrategy(QSqlTableModel.OnFieldChange)
        tableModel.select()
        headers = ("ID", "Name", "Street", "City", "Phone", "Email")

        for columnIndex, header in enumerate(headers):
            tableModel.setHeaderData(columnIndex, Qt.Horizontal, header)

        return tableModel
    
    def addContact(self, data):
        """Add a contact to the database"""
        rows = self.model.rowCount()
        self.model.insertRows(rows, 1)
        
        for column, field in enumerate(data):
            self.model.setData(self.model.index(rows, column + 1), field)
            
        self.model.submitAll()
        self.model.select()
        
    def deleteContact(self, row):
        """Remove a contact from the database"""
        self.model.removeRow(row)
        self.model.submitAll()
        self.model.select()

    def exportToPdf(self, row):
        """Export contact information to PDF form field"""
        # Create empty lists to store all the column headers and column content
        row_data_dict = {}
        column_header_list = []
        column_content_list = []
        
        # Go through the columns of the selected row of the contact table 
        # and save the column headers and content in lists
        for column in range (self.model.columnCount()):
            column_header = self.model.headerData(column, Qt.Horizontal)
            column_header_list.append(column_header)
            
            column_content = self.model.record(row).value(column)
            column_content_list.append(column_content)
            
            # Merge the two lists together into a dictionary
            row_data_dict[column_header_list[column]] = column_content_list[column]

        # Call function to fill out PDF forms
        fill_pdf(row_data_dict)

    def clearContacts(self):
        """Remove all contacts in the database"""
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.removeRows(0, self.model.rowCount())
        self.model.submitAll()
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()

