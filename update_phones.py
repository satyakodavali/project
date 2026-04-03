import sqlite3
import os

db_path = 'c:/Users/LENOVO/NewCollegeChatBot/college-portal/nsrit_portal.db'
if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Working numbers provided by user
updates = [
    ('9398344060', '24CSE100'),
    ('9182995461', '21CIVIL101'),
    ('9542138529', '21ECE102'),
    ('9391549259', '21CIVIL103')
]

for phone, roll in updates:
    cursor.execute("UPDATE students SET parents_mobile = ? WHERE roll_no = ?", (phone, roll))
    print(f"Updated {roll} with phone {phone}")

conn.commit()
conn.close()
print("Database update complete.")
