import sqlite3

rolls = ['24MECH115', '24MECH139', '24EEE119', '24EEE143', '24IT123', '24IT147']
db_path = 'nsrit_portal.db'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

for roll in rolls:
    cursor.execute("SELECT sgpa, cgpa FROM semester_results WHERE student_roll_no = ? AND semester = '1-1'", (roll,))
    res = cursor.fetchone()
    if res:
        print(f"{roll}: Found Sem 1-1. SGPA: {res[0]}, CGPA: {res[1]}")
    else:
        print(f"{roll}: NOT FOUND")

conn.close()
