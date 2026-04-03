import sqlite3
from werkzeug.security import generate_password_hash
import os

db_path = 'nsrit_portal.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Correct hash for Pass123!
    hashed_pw = generate_password_hash("Pass123!")
    print(f"Updating all students to hashed password: {hashed_pw[:20]}...")
    
    cursor.execute("UPDATE students SET password_hash = ?", (hashed_pw,))
    conn.commit()
    print(f"Updated {cursor.rowcount} students.")
    
    conn.close()
else:
    print(f"Database {db_path} not found")
