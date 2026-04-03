from werkzeug.security import check_password_hash
import sqlite3
import os

db_path = 'nsrit_portal.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    pwd = 'Pass123!'
    
    def test_login(username):
        # Emulate the logic in auth_routes.py
        cursor.execute("SELECT roll_no, password_hash FROM students WHERE UPPER(roll_no) = UPPER(?)", (username,))
        row = cursor.fetchone()
        if row:
            is_correct = check_password_hash(row['password_hash'], pwd)
            return f"Username: {username} -> Result: {'Success' if is_correct else 'Wrong Password'} (Found roll: {row['roll_no']})"
        return f"Username: {username} -> Result: Not Found"

    
    
    conn.close()
else:
    print("Database not found")
