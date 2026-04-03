import sqlite3
import random

rolls = ['24MECH115', '24MECH139', '24EEE119', '24EEE143', '24IT123', '24IT147']
db_path = 'nsrit_portal.db'

def add_performance():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    for roll in rolls:
        # Get branch
        cursor.execute("SELECT branch FROM students WHERE roll_no = ?", (roll,))
        res = cursor.fetchone()
        if not res: continue
        branch = res[0]
        
        # Get subjects for 1-1 for this branch
        cursor.execute("SELECT id, credits FROM subjects WHERE semester = '1-1' AND branch = ?", (branch,))
        subjects = cursor.fetchall()
        
        if not subjects:
            print(f"No subjects found for {branch} sem 1-1")
            continue
            
        # 1. Add Semester Results and Marks if missing
        cursor.execute("SELECT id FROM semester_results WHERE student_roll_no = ? AND semester = '1-1'", (roll,))
        if not cursor.fetchone():
            total_gp_credits = 0
            total_credits = 0
            
            for sub_id, credits in subjects:
                grade = random.choice(['O', 'A+', 'A', 'B+', 'B'])
                gp = {'O':10, 'A+':9, 'A':8, 'B+':7, 'B':6}[grade]
                cursor.execute("INSERT INTO marks (student_roll_no, subject_id, grade, grade_point, credits) VALUES (?, ?, ?, ?, ?)",
                             (roll, sub_id, grade, gp, credits))
                if credits > 0:
                    total_gp_credits += gp * credits
                    total_credits += credits
            
            sgpa = round(total_gp_credits / total_credits, 2) if total_credits > 0 else 0.0
            percentage = round(sgpa * 9.5, 2)
            
            cursor.execute("""
                INSERT INTO semester_results (student_roll_no, semester, sgpa, cgpa, total_credits, percentage) 
                VALUES (?, '1-1', ?, ?, ?, ?)
            """, (roll, sgpa, sgpa, total_credits, percentage))
            
            # Update CGPA Table
            cursor.execute("SELECT cgpa FROM cgpa WHERE student_roll_no = ?", (roll,))
            if cursor.fetchone():
                cursor.execute("UPDATE cgpa SET cgpa = ?, total_credits = ?, total_percentage = ? WHERE student_roll_no = ?",
                             (sgpa, total_credits, percentage, roll))
            else:
                cursor.execute("INSERT INTO cgpa (student_roll_no, cgpa, total_credits, total_percentage) VALUES (?, ?, ?, ?)",
                             (roll, sgpa, total_credits, percentage))
            print(f"Added semester results for {roll}")

        # 2. Add Attendance if missing
        for sub_id, _ in subjects:
            cursor.execute("SELECT id FROM attendance WHERE student_roll_no = ? AND subject_id = ?", (roll, sub_id))
            if not cursor.fetchone():
                held = random.randint(40, 50)
                attended = random.randint(30, held)
                cursor.execute("INSERT INTO attendance (student_roll_no, subject_id, classes_held, classes_attended) VALUES (?, ?, ?, ?)",
                             (roll, sub_id, held, attended))
        print(f"Ensured attendance for {roll}")

        # 3. Add Internal Marks if missing
        for sub_id, _ in subjects:
            cursor.execute("SELECT id FROM internal_marks WHERE student_roll_no = ? AND subject_id = ?", (roll, sub_id))
            if not cursor.fetchone():
                mid1 = random.randint(15, 25)
                mid2 = random.randint(15, 25)
                assign = random.randint(4, 5)
                online = random.randint(8, 10)
                lab = random.randint(18, 25)
                cursor.execute("""
                    INSERT INTO internal_marks (student_roll_no, subject_id, mid1, mid2, assignments, online_tests, lab_marks) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (roll, sub_id, mid1, mid2, assign, online, lab))
        print(f"Ensured internal marks for {roll}")
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    add_performance()
