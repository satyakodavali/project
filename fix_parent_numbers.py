import sqlite3
import random
import os

db_path = 'nsrit_portal.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    test_mobile_numbers = ["9398344060", "9182995461", "9542138529", "9391549259"]
    
    cursor.execute("SELECT roll_no FROM students")
    students = cursor.fetchall()
    
    print(f"Updating {len(students)} students with random test numbers...")
    for (roll,) in students:
        num = random.choice(test_mobile_numbers)
        cursor.execute("UPDATE students SET parents_mobile = ? WHERE roll_no = ?", (num, roll))
    
    conn.commit()
    print("Update complete.")
    conn.close()
else:
    print(f"Database {db_path} not found")
