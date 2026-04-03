import sqlite3
import os

db_path = 'nsrit_portal.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT description, start_date FROM academic_calendar")
    rows = cursor.fetchall()
    for row in rows:
        print(f"{row[0]} | {row[1]}")
    conn.close()
else:
    print("Database not found")
