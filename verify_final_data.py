import sqlite3

rolls = ['24MECH115', '24MECH139', '24EEE119', '24EEE143', '24IT123', '24IT147']
db_path = 'nsrit_portal.db'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

for roll in rolls:
    # Check semester results
    cursor.execute("SELECT sgpa FROM semester_results WHERE student_roll_no = ? AND semester = '1-1'", (roll,))
    sem = cursor.fetchone()
    
    # Check attendance
    cursor.execute("SELECT COUNT(*) FROM attendance a JOIN subjects s ON a.subject_id = s.id WHERE a.student_roll_no = ? AND s.semester = '1-1'", (roll,))
    att = cursor.fetchone()[0]
    
    # Check internal marks
    cursor.execute("SELECT COUNT(*) FROM internal_marks i JOIN subjects s ON i.subject_id = s.id WHERE i.student_roll_no = ? AND s.semester = '1-1'", (roll,))
    int_m = cursor.fetchone()[0]
    
    status = "OK" if sem and att == 8 and int_m == 8 else "MISSING"
    print(f"{roll}: Results={bool(sem)}, Att={att}, IntMarks={int_m} -> {status}")

conn.close()
