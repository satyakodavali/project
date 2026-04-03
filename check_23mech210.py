import sqlite3

db_path = 'nsrit_portal.db'
roll = '23MECH210'

conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute("SELECT roll_no, name, parents_mobile FROM students WHERE UPPER(roll_no) = UPPER(?)", (roll,))
row = cursor.fetchone()

if row:
    print(f"Student Found:")
    print(f"Roll: '{row['roll_no']}' (Length: {len(row['roll_no'])})")
    print(f"Name: {row['name']}")
    print(f"Parent Mobile: '{row['parents_mobile']}' (Length: {len(row['parents_mobile']) if row['parents_mobile'] else 0})")
else:
    print("Student NOT found in database.")

conn.close()
