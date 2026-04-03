import sqlite3
import os
from config import Config

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_db_connection():
    try:
        # ABSOLUTE PATH to ensure consistency regardless of how the app is started
        db_path = r'c:\Users\LENOVO\NewCollegeChatBot\college-portal\backend\nsrit_portal.db'
        
        # Connect to local SQLite file
        conn = sqlite3.connect(db_path)
        
        # Override cursor factory so it behaves like MySQL's dictionary=True
        conn.row_factory = dict_factory
        return conn
    except sqlite3.Error as err:
        print(f"Error connecting to SQLite: {err}")
        return None
