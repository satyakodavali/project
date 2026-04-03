from werkzeug.security import check_password_hash
import sqlite3
import os

db_path = 'nsrit_portal.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    user = 'admin'
    pwd = 'Admin12!'
    
    cursor.execute("SELECT password_hash FROM admins WHERE username = ?", (user,))
    row = cursor.fetchone()
    
    if row:
        stored_hash = row['password_hash']
        is_correct = check_password_hash(stored_hash, pwd)
        print(f"Admin User: {user}")
        print(f"Password Check ('{pwd}'): {is_correct}")
    else:
        print(f"Admin {user} not found")
    
    conn.close()
else:
    print("Database not found")
