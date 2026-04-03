import sqlite3
import os

db_path = 'nsrit_portal.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    roll = '24CSE100'
    cursor.execute("SELECT * FROM students WHERE UPPER(roll_no) = UPPER(?)", (roll,))
    row = cursor.fetchone()
    
    if row:
        print(f"Found student: {row['roll_no']}")
        print(f"Name: {row['name']}")
        print(f"Hash: {row['password_hash']}")
    else:
        print(f"Student {roll} not found in {os.path.abspath(db_path)}")
    
    conn.close()
else:
    print(f"Database {db_path} not found")
