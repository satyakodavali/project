from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import os

db_path = 'nsrit_portal.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    roll = '24CSE100'
    pwd = 'Pass123!'
    
    cursor.execute("SELECT password_hash FROM students WHERE roll_no = ?", (roll,))
    row = cursor.fetchone()
    
    if row:
        stored_hash = row['password_hash']
        is_correct = check_password_hash(stored_hash, pwd)
        print(f"Roll: {roll}")
        print(f"Stored Hash: {stored_hash}")
        print(f"Password Check ('{pwd}'): {is_correct}")
        
        # Also check lowercase vs uppercase
        cursor.execute("SELECT password_hash FROM students WHERE roll_no = '24cse100'")
        row_low = cursor.fetchone()
        print(f"Lowercase query result: {'Found' if row_low else 'Not Found'}")
    else:
        print(f"Student {roll} not found")
    
    conn.close()
else:
    print("Database not found")
