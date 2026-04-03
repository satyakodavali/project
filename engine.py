import re
import random
from utils.db import get_db_connection
from .predictions import attendance_logic, marks_prediction, cgpa_backlog_logic, fees_warning_logic, backlog_exam_message
from .scheduler import generate_mid_timetable, generate_sem_timetable, get_backlog_exam_schedule

# General knowledge base
COLLEGE_INFO = {
    "location": "NSRIT is located in Visakhapatnam, Andhra Pradesh.",
    "admission": "Admission is based on EAMCET ranks and management quota. Please visit the admissions section for details.",
    "courses": "We offer B.Tech in CSE, ECE, CIVIL, MECH, EEE, and IT.",
    "placements": "NSRIT has an excellent placement record with top MNCs like TCS, Infosys, and Wipro.",
    "facilities": "We provide state-of-the-art labs, a central library, sports complexes, and hostel facilities.",
    "departments": "Our departments include Computer Science, Electronics, Civil, Mechanical, and Electrical."
}

def clean_text(text):
    return re.sub(r'[^\w\s]', '', text).lower()

def check_authorization_violation(query, user_context):
    """Ensure the user isn't asking for another student's info."""
    query_lower = query.lower()
    
    # Check if querying for another person's specific academic info
    sensitive_keywords = ['cgpa', 'sgpa', 'marks', 'attendance', 'fees']
    if any(k in query_lower for k in sensitive_keywords):
        # Allow checking own
        if "my " in query_lower or "mine" in query_lower:
            return False
            
        # Very strict simple rule: if there's a name or "someone else's" word
        # In a real NLP agent this would use NER to detect names
        names = ["suresh", "ravi", "ramesh", "lakshmi", "priya", "his", "her", "their", "'s"]
        for n in names:
            if n in query_lower:
                return True
    return False

def get_student_backlogs_list(roll_no, cgpa, current_semester, branch, cursor):
    """Integrated logic to fetch real backlogs and simulate others based on CGPA."""
    # 1. Previous Semesters Mapping
    sem_map = ['1-1', '1-2', '2-1', '2-2', '3-1', '3-2', '4-1', '4-2']
    try:
        curr_idx = sem_map.index(current_semester)
    except ValueError:
        curr_idx = 0
    prev_sems = sem_map[:curr_idx]
    
    # 2. Fetch Actual Failures (Grade 'F')
    cursor.execute("""
        SELECT s.name, s.semester, s.id as subject_id
        FROM marks m
        JOIN subjects s ON m.subject_id = s.id
        WHERE m.student_roll_no = ? AND m.grade = 'F'
    """, (roll_no,))
    backlogs = [{"name": r['name'], "semester": r['semester'], "is_real": True, "subject_id": r['subject_id']} for r in cursor.fetchall()]
    
    # 3. Dynamic Generation based on CGPA if needed
    target_count = 0
    if 7.0 <= cgpa < 8.0: target_count = random.Random(roll_no).randint(1, 3)
    elif 6.0 <= cgpa < 7.0: target_count = random.Random(roll_no).randint(4, 7)
    elif cgpa < 6.0: target_count = random.Random(roll_no).randint(8, 12)
    
    if len(backlogs) < target_count:
        # Fetch all potential subjects from previous semesters for this branch
        placeholders = ', '.join(['?'] * len(prev_sems))
        if prev_sems:
            cursor.execute(f"SELECT id, name, semester FROM subjects WHERE branch = ? AND semester IN ({placeholders})", (branch, *prev_sems))
            all_prev_subs = cursor.fetchall()
            
            # Exclude already real backlogs
            existing_ids = {b['subject_id'] for b in backlogs}
            pool = [s for s in all_prev_subs if s['id'] not in existing_ids]
            
            # Seed random with roll_no for consistency
            rng = random.Random(roll_no)
            needed = target_count - len(backlogs)
            if pool:
                simulated = rng.sample(pool, min(len(pool), needed))
                for s in simulated:
                    backlogs.append({"name": s['name'], "semester": s['semester'], "is_real": False, "subject_id": s['id']})
    
    return backlogs

def get_student_data(roll_no, user_query):
    conn = get_db_connection()
    if not conn:
        return "Database connection error."
        
    cursor = conn.cursor()
    q = user_query.lower()
    try:
        # Fetch basic student info for context
        cursor.execute("SELECT * FROM students WHERE roll_no = ?", (roll_no,))
        student = cursor.fetchone()
        if not student:
            return "Student record not found."

        # 1. Fees
        if 'total fee due' in q or ('fee' in q and 'due' in q and 'hostel' not in q):
            cursor.execute("SELECT (tuition_fees + convener_fees + management_fees + hostel_fees - paid_fees) as due FROM fees WHERE student_roll_no = ?", (roll_no,))
            fee = cursor.fetchone()
            due = fee['due'] if fee else 0
            warning = fees_warning_logic(due)
            return f"Your total fee due is Rs. {due}. {warning}"
        
        elif 'hostel fee' in q:
            cursor.execute("SELECT hostel_fees FROM fees WHERE student_roll_no = ?", (roll_no,))
            f = cursor.fetchone()
            return f"Your hostel fee is Rs. {f['hostel_fees'] if f else 0}."

        elif 'fee payment deadline' in q or ('by when' in q and 'fee' in q):
            cursor.execute("SELECT due_date FROM fees WHERE student_roll_no = ? ORDER BY due_date DESC LIMIT 1", (roll_no,))
            f = cursor.fetchone()
            return f"The fee payment deadline is {f['due_date']}." if f else "No deadline currently listed."

        # 2. Academic Performance & CGPA
        elif 'cgpa' in q:
            cursor.execute("SELECT cgpa, total_credits FROM cgpa WHERE student_roll_no = ?", (roll_no,))
            c = cursor.fetchone()
            if not c: return "CGPA data not available."
            res = cgpa_backlog_logic(float(c['cgpa']))
            if 'total credits' in q:
                return f"Your current CGPA is {c['cgpa']} and total credits earned are {c['total_credits']}. Risk: {res['risk_level']}. {res['motivation']}"
            return f"Your current CGPA is {c['cgpa']}. Risk: {res['risk_level']}. {res['motivation']}"
        
        elif 'latest sgpa' in q or 'latest semester' in q:
            cursor.execute("SELECT semester, sgpa FROM semester_results WHERE student_roll_no = ? ORDER BY semester DESC LIMIT 1", (roll_no,))
            s = cursor.fetchone()
            return f"Your latest SGPA for semester {s['semester'] if s else ''} is {s['sgpa'] if s else 'not available'}."
        
        elif 'previous sgpa' in q or 'previous semester sgpa' in q:
            cursor.execute("SELECT semester, sgpa FROM semester_results WHERE student_roll_no = ? ORDER BY semester DESC LIMIT 1 OFFSET 1", (roll_no,))
            s = cursor.fetchone()
            if s:
                return f"Your previous semester ({s['semester']}) SGPA was {s['sgpa']}."
            return "Previous semester SGPA is not available."
            
        elif 'show my previous cgpa' in q or 'previous cgpa' in q:
            cursor.execute("SELECT semester FROM semester_results WHERE student_roll_no = ? ORDER BY semester DESC", (roll_no,))
            sems = cursor.fetchall()
            if not sems:
                return "You do not have any completed semester results."
            
            response = "Select semester:\n\n"
            for sem in sems:
                response += f"[[GET_SEM_CGPA_{sem['semester']}]]\n"
            return response
            
        elif q.startswith('get_sem_cgpa_'):
            sem = q.replace('get_sem_cgpa_', '').strip()
            # Fetch backlogs to sync
            cursor.execute("SELECT cgpa FROM cgpa WHERE student_roll_no = ?", (roll_no,))
            c_row = cursor.fetchone()
            c_val = float(c_row['cgpa']) if c_row else 7.0
            backlogs_list = get_student_backlogs_list(roll_no, c_val, student['current_semester'], student['branch'], cursor)
            backlog_ids = {b['subject_id'] for b in backlogs_list}

            try:
                # User requested columns: sgpa, cgpa, credits. We ALSO fetch marks detail for UI fix.
                cursor.execute("SELECT sgpa, cgpa, total_credits FROM semester_results WHERE student_roll_no = ? AND semester = ?", (roll_no, sem))
                res = cursor.fetchone()
                if res:
                    msg = f"Semester: {sem}\nSGPA: {res['sgpa']}\nCGPA: {res['cgpa']}\nTotal Credits: {res['total_credits']}\n\n"
                    # Fetch subject-wise details for this semester
                    cursor.execute("""
                        SELECT s.name, m.grade, m.credits, s.id
                        FROM marks m
                        JOIN subjects s ON m.subject_id = s.id
                        WHERE m.student_roll_no = ? AND s.semester = ?
                    """, (roll_no, sem))
                    marks_details = cursor.fetchall()
                    
                    if marks_details:
                        msg += "| Subject | Grade | Credits |\n| :--- | :--- | :--- |\n"
                        for m in marks_details:
                            # UI FIX: If subject is in backlogs, show RED F and 0 credits
                            if m['id'] in backlog_ids:
                                g = "<span style='color:red'>F</span>"
                                cr = "<span style='color:red'>0</span>"
                            else:
                                g = m['grade']
                                cr = m['credits']
                            msg += f"| {m['name']} | {g} | {cr} |\n"
                    return msg
                return f"Results not found for semester {sem}."
            except Exception:
                # Fallback if marks table or columns missing
                cursor.execute("SELECT sgpa FROM semester_results WHERE student_roll_no = ? AND semester = ?", (roll_no, sem))
                res = cursor.fetchone()
                if res:
                    return f"Semester: {sem}\nSGPA: {res['sgpa']}"
                return f"Results not found for semester {sem}."

        # 3. Backlogs logic
        elif 'backlog' in q:
            cursor.execute("SELECT cgpa FROM cgpa WHERE student_roll_no = ?", (roll_no,))
            c = cursor.fetchone()
            cgpa_val = float(c['cgpa']) if c else 0
            
            backlogs = get_student_backlogs_list(roll_no, cgpa_val, student['current_semester'], student['branch'], cursor)
            
            if not backlogs:
                return "You current backlog status: **None**. Keep up the good work!"

            # 1. Backlog Table
            response = "### Current Backlogs\n"
            response += "| Subject | Semester |\n| :--- | :--- |\n"
            for b in backlogs:
                response += f"| {b['name']} | {b['semester']} |\n"
            
            # 2. Motivation Message (FIXED)
            response += "\nWith better performance in upcoming exams, you can easily improve. Focus on weak subjects and practice regularly.\n"
            
            # 3. Exam Reminder (NOTE)
            first_backlog = backlogs[0]
            sched = get_backlog_exam_schedule(first_backlog['name'], first_backlog['semester'])
            response += f"\n### NOTE\n{sched}"
            
            return response

        # 4. Course & Class Details
        elif 'subjects' in q:
            cursor.execute("""
                SELECT DISTINCT s.id, s.name
                FROM attendance a
                JOIN subjects s ON a.subject_id = s.id
                WHERE a.student_roll_no = ? AND s.semester = ?
            """, (roll_no, student['current_semester']))
            attendance_subs = cursor.fetchall()
            
            if not attendance_subs:
                return "No timetable data available for your semester"
                
            sub_details = []
            for s in attendance_subs:
                cursor.execute("""
                    SELECT DISTINCT t.name 
                    FROM timetable tt 
                    JOIN teachers t ON tt.teacher_id = t.teacher_id
                    WHERE tt.subject_id = ? AND tt.branch = ? AND tt.year = ? AND tt.section = ?
                """, (s['id'], student['branch'], student['year'], student['section']))
                t_row = cursor.fetchone()
                teacher_name = t_row['name'] if t_row else "Assigned Faculty"
                sub_details.append(f"{s['name']} | {teacher_name}")
            
            return f"Your subjects for Semester {student['current_semester']}:\n" + "\n".join(sub_details)

        elif 'branch' in q or 'year' in q or 'section' in q:
            return f"Your branch is {student['branch']}, you are in year {student['year']}, section {student['section']}."

        # 5. Faculty
        elif 'mentor' in q:
            cursor.execute("""
                SELECT t.name FROM mentors m 
                JOIN teachers t ON m.teacher_id = t.teacher_id 
                WHERE m.student_roll_no = ?
            """, (roll_no,))
            m = cursor.fetchone()
            return f"Your assigned mentor is {m['name'] if m else 'not assigned'}."

        elif 'class teacher' in q:
            cursor.execute("""
                SELECT t.name FROM teachers t
                JOIN class_teachers ct ON t.teacher_id = ct.teacher_id
                WHERE ct.branch = ? AND ct.year = ? AND ct.section = ?
            """, (student['branch'], student['year'], student['section']))
            t = cursor.fetchone()
            return f"Your class teacher is {t['name'] if t else 'not assigned'}."

        # 6. Attendance prediction
        elif 'attendance' in q:
            cursor.execute("""
                SELECT SUM(a.classes_held) as held, SUM(a.classes_attended) as attended 
                FROM attendance a
                JOIN subjects s ON a.subject_id = s.id
                WHERE a.student_roll_no = ? AND s.semester = ?
            """, (roll_no, student['current_semester'] if student.get('current_semester') else '1-1'))
            a = cursor.fetchone()
            if not a or not a['held']: return "Attendance data not available for current semester."
            
            res = attendance_logic(a['attended'], a['held'])
            return f"Your Attendance: {res['percentage']}% ({a['attended']}/{a['held']} classes).\nPrediction: {res['prediction']}.\n{res['suggestion']}"

        # 7. Internal Marks Prediction
        elif 'internal marks' in q:
            cursor.execute("""
                SELECT s.name, i.mid1, i.mid2 FROM internal_marks i
                JOIN subjects s ON i.subject_id = s.id
                WHERE i.student_roll_no = ?
            """, (roll_no,))
            marks = cursor.fetchall()
            if not marks: return "Internal marks are not yet uploaded."
            
            m_list = []
            for m in marks:
                pred = marks_prediction(m['mid1'], m['mid2'])
                m_list.append(f"{m['name']}: Mid1({m['mid1']}), Mid2({m['mid2']}). Prediction: {pred['risk']}. {pred['message']}")
            return "Your internal marks and predictions:\n" + "\n".join(m_list)

        # 8. Exams & Dynamic Scheduling
        elif 'mid exam' in q or 'next mid' in q or 'mid 1' in q or 'mid 2' in q or 'semester exam' in q or 'sem 1' in q or 'sem 2' in q:
            sem_name = student['current_semester'] or '1-1'
            is_odd = any(s in sem_name for s in ['1', '3', '5', '7'])
            suffix = "- Sem I" if is_odd else "- Sem II"

            cursor.execute("SELECT name FROM subjects WHERE branch = ? AND semester = ?", (student['branch'], sem_name))
            subjects = [r['name'] for r in cursor.fetchall()]
            if not subjects: subjects = ["Subject 1", "Subject 2", "Subject 3", "Subject 4", "Subject 5"]

            def fetch_exam_date(desc):
                cursor.execute("SELECT start_date FROM academic_calendar WHERE description LIKE ?", (f"%{desc}%",))
                row = cursor.fetchone()
                return row['start_date'] if row else "2026-04-01"

            if 'mid 1' in q:
                d = fetch_exam_date(f"MID-I Exams {suffix}")
                tt = generate_mid_timetable(d, subjects)
                tt_str = "\n".join([f"{t['date']}: {t['subject']}" for t in tt])
                return f"MID-I Timetable ({sem_name}):\n{tt_str}\nGood luck for your exams! Prepare well."
            
            if 'mid 2' in q:
                d = fetch_exam_date(f"MID-II Exams {suffix}")
                tt = generate_mid_timetable(d, subjects)
                tt_str = "\n".join([f"{t['date']}: {t['subject']}" for t in tt])
                return f"MID-II Timetable ({sem_name}):\n{tt_str}\nGood luck for your exams! Prepare well."

            if 'semester exam' in q or 'sem ' in q:
                d = fetch_exam_date(f"Semester End Exams {suffix}")
                tt = generate_sem_timetable(d, subjects)
                tt_str = "\n".join([f"{t['date']}: {t['subject']}" for t in tt])
                return f"Semester End Timetable ({sem_name}):\n{tt_str}\nGood luck for your exams! Prepare well."
            
            d1 = fetch_exam_date(f"MID-I Exams {suffix}")
            d2 = fetch_exam_date(f"MID-II Exams {suffix}")
            ds = fetch_exam_date(f"Semester End Exams {suffix}")
            return f"Upcoming Exam Cycles ({sem_name}):\n1. MID-I: Starts {d1}\n2. MID-II: Starts {d2}\n3. Semester End: Starts {ds}\nGood luck for your exams! Prepare well."

        # 9. Timetable
        elif 'timetable' in q or 'period' in q:
            cursor.execute("""
                SELECT DISTINCT s.id FROM attendance a 
                JOIN subjects s ON a.subject_id = s.id 
                WHERE a.student_roll_no = ? AND s.semester = ?
            """, (roll_no, student['current_semester']))
            att_ids = [r['id'] for r in cursor.fetchall()]
            
            if not att_ids: return "No timetable data available for your semester"

            cursor.execute("""
                SELECT tt.day, tt.period, s.name as subject, t.name as teacher, tt.subject_id
                FROM timetable tt 
                JOIN subjects s ON tt.subject_id = s.id 
                JOIN teachers t ON tt.teacher_id = t.teacher_id
                WHERE tt.branch = ? AND tt.year = ? AND tt.section = ? AND s.semester = ?
                ORDER BY CASE 
                    WHEN day='Monday' THEN 1 WHEN day='Tuesday' THEN 2 WHEN day='Wednesday' THEN 3 
                    WHEN day='Thursday' THEN 4 WHEN day='Friday' THEN 5 WHEN day='Saturday' THEN 6 END, tt.period
            """, (student['branch'], student['year'], student['section'], student['current_semester']))
            tt_all = cursor.fetchall()
            
            if not tt_all: return "No timetable data available for your semester"
            
            times = {
                1: "09:00 AM - 09:50 AM", 2: "09:50 AM - 10:40 AM", 3: "10:40 AM - 11:30 AM",
                4: "11:30 AM - 12:20 PM", 5: "01:10 PM - 02:00 PM", 6: "02:00 PM - 02:50 PM",
                7: "02:50 PM - 3:40 PM", 8: "03:40 PM - 04:30 PM"
            }
            
            periods = {"1st": 1, "2nd": 2, "3rd": 3, "4th": 4, "5th": 5, "6th": 6, "7th": 7, "8th": 8}
            p_num = None
            for pk, pv in periods.items():
                if pk in q:
                    p_num = pv
                    break
            
            if 'lunch' in q: return "Lunch break | 12:20 PM - 01:10 PM"
            
            import datetime
            today = datetime.datetime.now().strftime('%A')
            if today in ["Sunday", "Saturday"]: today = "Monday"
            
            if p_num:
                p_info = next((t for t in tt_all if t['day'] == today and t['period'] == p_num), None)
                if p_info and p_info['subject_id'] in att_ids:
                    return f"{p_info['subject']} | {p_info['teacher']} | {times.get(p_num)}"
                return "No period info available."

            today_tt = [t for t in tt_all if t['day'] == today and t['subject_id'] in att_ids]
            if not today_tt: return "No classes scheduled for today."
            
            resp = f"Timetable for {today} (Semester {student['current_semester']}):\n"
            for t in today_tt:
                resp += f"{t['subject']} | {t['teacher']} | {times.get(t['period'])}\n"
            resp += "Lunch break | 12:20 PM - 01:10 PM"
            return resp

        elif 'outing' in q:
            cursor.execute("SELECT date, out_time, in_time, reason FROM outing_records WHERE roll_number = ? ORDER BY date DESC LIMIT 3", (roll_no,))
            outings = cursor.fetchall()
            if not outings: return "No outing history found."
            o_list = "; ".join([f"{o['date']} ({o['reason']}) - Out: {o['out_time']} In: {o['in_time']}" for o in outings])
            return f"Your recent outings: {o_list}."

        return "I can help you with your CGPA, attendance, fees, backlogs, timetable, outings, and more. What would you like to know?"

    finally:
        cursor.close()
        conn.close()
    
    return "I couldn't fetch that information right now."

def handle_authenticated_query(query, roll_no):
    q = query.lower()
    
    # Matching keywords for all 26 predefined questions + variations
    keywords = [
        'fee', 'due', 'paid', 'deadline', 'cgpa', 'sgpa', 'backlog', 
        'mentor', 'class teacher', 'teachers', 'attendance', 'classes',
        'mid exam', 'semester exam', 'exam date', 'mid', 'sem', 'branch', 'year', 'section',
        'subject', 'internal marks', 'credits', 'timetable', 'calendar', 'hostel', 'outing', 'period',
        'who handles', 'handle'
    ]
    
    if any(k in q for k in keywords):
        return get_student_data(roll_no, query)
        
    if q.startswith("get_sem_cgpa_"):
        return get_student_data(roll_no, query)
        
    if "branch" in q or "year" in q:
        return f"You are currently logged in with Roll Number: {roll_no}. Your specific academic details are visible in your profile."

    return process_general_query(query)

def process_general_query(query):
    q = query.lower()
    if "location" in q or "where" in q:
        return COLLEGE_INFO["location"]
    elif "admission" in q or "join" in q:
        return COLLEGE_INFO["admission"]
    elif "course" in q or "branch" in q:
        return COLLEGE_INFO["courses"]
    elif "placement" in q:
        return COLLEGE_INFO["placements"]
    elif "facility" in q or "hostel" in q:
        return COLLEGE_INFO["facilities"]
    elif "department" in q:
        return COLLEGE_INFO["departments"]
    elif "hi" in q or "hello" in q:
        return "Hello! I am the NSRIT Assistant. How can I help you today?"
        
    return "I am an AI assistant for NSRIT. I can answer questions about your attendance, fees, marks, and college info."

def process_query(query, user_context):
    if check_authorization_violation(query, user_context):
        return "You can only access your own academic information for security reasons."
        
    is_authorized = user_context.get('role') in ['student', 'parent']
    roll_no = user_context.get('roll_no')
    
    if is_authorized and roll_no:
        sensitive = [
            'cgpa', 'sgpa', 'attendance', 'fee', 'mentor', 'subject', 'backlog', 
            'exam', 'teacher', 'branch', 'year', 'timetable', 'period', 'calendar', 'outing',
            'who handles', 'handle'
        ]
        if any(s in query.lower() for s in sensitive):
            return handle_authenticated_query(query, roll_no)
            
    return process_general_query(query)

