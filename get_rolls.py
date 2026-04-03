import sqlite3
import os

db_path = 'nsrit_portal.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT roll_no, name, branch, year FROM students LIMIT 15")
    rows = cursor.fetchall()
    print("Roll No | Name | Branch | Year")
    print("-" * 40)
    for r in rows:
        print(f"{r[0]} | {r[1]} | {r[2]} | {r[3]}")
    conn.close()
else:
    print(f"Database {db_path} not found")
