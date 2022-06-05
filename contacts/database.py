# -*- coding: utf-8 -*-
"""
Created on Sat May 14 16:45:54 2022

@author: ph1g0
"""

"""This module provides a database connection"""

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery



def _createContactsTable():
    """Create the contacts table in the database"""
    createTableQuery = QSqlQuery()
    return createTableQuery.exec(
        """
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            name1 VARCHAR(50) NOT NULL,
            name2 VARCHAR(50) NOT NULL,
            street VARCHAR(50) NOT NULL,
            city VARCHAR(50) NOT NULL,
            phone VARCHAR(50) NOT NULL,
            email VARCHAR(50) NOT NULL
        )
        """
    )

def createConnection(databaseName):
    """Create and open a database connection"""
    connection = QSqlDatabase.addDatabase("QSQLITE")
    connection.setDatabaseName(databaseName)

    if not connection.open():
        QMessageBox.warning(
            None,
            "Contact",
            f"Database Error: {connection.lastError().text()}",
        )
        return False

    _createContactsTable()
    return True
