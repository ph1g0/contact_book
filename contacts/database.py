# -*- coding: utf-8 -*-
"""
Created on Sat May 14 16:45:54 2022

@author: phigo
"""

"""This module provides a database connection"""

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

def _createContactsTable():
    """Create the contacts table in the database"""
    createTableQuery = QSqlQuery()
    return createTableQuery.exec_(
        """
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            name VARCHAR(40) NOT NULL,
            job VARCHAR(50),
            email VARCHAR(40) NOT NULL
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
