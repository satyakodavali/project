import sqlite3
import os

db_path = 'nsrit_portal.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT roll_no FROM students WHERE roll_no LIKE '23CIVIL%' LIMIT 5")
    rows = cursor.fetchall()
    print("Valid 23CIVIL examples:")
    for r in rows:
        print(r[0])
    conn.close()
else:
    print("DB not found")
