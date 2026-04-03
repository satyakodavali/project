from flask import Blueprint, jsonify, session
from utils.db import get_db_connection
from functools import wraps

student_bp = Blueprint('student_bp', __name__)

def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'] != 'student':
            return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403
        return f(*args, **kwargs)
    return decorated_function

@student_bp.route('/profile', methods=['GET'])
@student_required
def get_profile():
    roll_no = session.get('roll_no')
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM students WHERE roll_no = ?", (roll_no,))
        student = cursor.fetchone()
        if not student: return jsonify({'status': 'error', 'message': 'Not found'}), 404
        
        # Mentor Info
        cursor.execute("""
            SELECT t.name, t.department 
            FROM mentors m 
            JOIN teachers t ON m.teacher_id = t.teacher_id 
            WHERE m.student_roll_no = ?
        """, (roll_no,))
        student['mentor'] = cursor.fetchone()

        # Class Teacher
        cursor.execute("""
            SELECT t.name FROM teachers t
            JOIN class_teachers ct ON t.teacher_id = ct.teacher_id
            WHERE ct.branch = ? AND ct.year = ? AND ct.section = ?
        """, (student['branch'], student['year'], student['section']))
        student['class_teacher'] = cursor.fetchone()

        return jsonify({'status': 'success', 'data': student})
    finally:
        cursor.close()
        conn.close()

@student_bp.route('/attendance', methods=['GET'])
@student_required
def get_attendance():
    roll_no = session.get('roll_no')
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Table format: Subject, Held, Attended, Percentage
        cursor.execute("""
            SELECT s.name as subject, SUM(a.classes_held) as held, SUM(a.classes_attended) as attended
            FROM attendance a
            JOIN subjects s ON a.subject_id = s.id
            JOIN students st ON a.student_roll_no = st.roll_no
            WHERE a.student_roll_no = ? AND s.semester = st.current_semester
            GROUP BY s.name
        """, (roll_no,))
        records = cursor.fetchall()
        for r in records:
            r['percentage'] = round((r['attended'] / r['held']) * 100, 2) if r['held'] > 0 else 0
        return jsonify({'status': 'success', 'data': records})
    finally:
        cursor.close()
        conn.close()

@student_bp.route('/daily-attendance', methods=['GET'])
@student_required
def get_daily_attendance():
    roll_no = session.get('roll_no')
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM daily_attendance WHERE roll_number = ? ORDER BY date DESC", (roll_no,))
        return jsonify({'status': 'success', 'data': cursor.fetchall()})
    finally:
        cursor.close()
        conn.close()

@student_bp.route('/performance', methods=['GET'])
@student_required
def get_performance():
    roll_no = session.get('roll_no')
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT SUM(held) as total_held, SUM(attended) as total_attended FROM (
                SELECT SUM(a.classes_held) as held, SUM(a.classes_attended) as attended
                FROM attendance a
                JOIN subjects s ON a.subject_id = s.id
                JOIN students st ON a.student_roll_no = st.roll_no
                WHERE a.student_roll_no = ? AND s.semester = st.current_semester
                GROUP BY s.name
            ) as grouped
        """, (roll_no,))
        agg = cursor.fetchone()
        return jsonify({'status': 'success', 'data': agg})
    finally:
        cursor.close()
        conn.close()

@student_bp.route('/past-performance', methods=['GET'])
@student_required
def get_past_performance():
    roll_no = session.get('roll_no')
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM semester_results WHERE student_roll_no = ? ORDER BY semester", (roll_no,))
        sems = cursor.fetchall()
        
        for sem in sems:
            sem_name = sem['semester']
            # 1. External Marks
            cursor.execute("""
                SELECT s.subject_code, s.name, m.grade, m.credits 
                FROM marks m JOIN subjects s ON m.subject_id = s.id 
                WHERE m.student_roll_no = ? AND s.semester = ?
            """, (roll_no, sem_name))
            sem['marks'] = cursor.fetchall()
            
            # 2. Historical Attendance
            cursor.execute("""
                SELECT s.name as subject, a.classes_held as held, a.classes_attended as attended
                FROM attendance a JOIN subjects s ON a.subject_id = s.id
                WHERE a.student_roll_no = ? AND s.semester = ?
            """, (roll_no, sem_name))
            att_records = cursor.fetchall()
            for r in att_records:
                r['percentage'] = round((r['attended'] / r['held']) * 100, 2) if r['held'] > 0 else 0
            sem['attendance'] = att_records
            
            # 3. Historical Internals
            cursor.execute("""
                SELECT s.name as subject, im.* 
                FROM internal_marks im JOIN subjects s ON im.subject_id = s.id
                WHERE im.student_roll_no = ? AND s.semester = ?
            """, (roll_no, sem_name))
            sem['internals'] = cursor.fetchall()

        cursor.execute("SELECT * FROM cgpa WHERE student_roll_no = ?", (roll_no,))
        overall = cursor.fetchone()
        
        # Issue 7/8 - Make sure to merge cgpa correctly or at least send whatever we have so frontend works.
        return jsonify({'status': 'success', 'data': {'semesters': sems, 'cgpa': overall}})
    finally:
        cursor.close()
        conn.close()

@student_bp.route('/internal-marks', methods=['GET'])
@student_required
def get_internal_marks():
    roll_no = session.get('roll_no')
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT s.name as subject, im.* 
            FROM internal_marks im
            JOIN subjects s ON im.subject_id = s.id
            JOIN students st ON im.student_roll_no = st.roll_no
            WHERE im.student_roll_no = ? AND s.semester = st.current_semester
        """, (roll_no,))
        return jsonify({'status': 'success', 'data': cursor.fetchall()})
    finally:
        cursor.close()
        conn.close()

@student_bp.route('/backlogs', methods=['GET'])
@student_required
def get_backlogs():
    roll_no = session.get('roll_no')
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT s.subject_code as sem_subject, s.name, b.semester
            FROM backlogs b
            JOIN subjects s ON b.subject_id = s.id
            WHERE b.student_roll_no = ?
        """, (roll_no,))
        return jsonify({'status': 'success', 'data': cursor.fetchall()})
    finally:
        cursor.close()
        conn.close()

@student_bp.route('/fees', methods=['GET'])
@student_required
def get_fees():
    roll_no = session.get('roll_no')
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM fees WHERE student_roll_no = ?", (roll_no,))
        return jsonify({'status': 'success', 'data': cursor.fetchall()})
    finally:
        cursor.close()
        conn.close()

@student_bp.route('/hostel', methods=['GET'])
@student_required
def get_hostel():
    roll_no = session.get('roll_no')
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM hostel_records WHERE student_roll_no = ?", (roll_no,))
        return jsonify({'status': 'success', 'data': cursor.fetchone()})
    finally:
        cursor.close()
        conn.close()

@student_bp.route('/outings', methods=['GET'])
@student_required
def get_outings():
    roll_no = session.get('roll_no')
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM outing_records WHERE roll_number = ? ORDER BY date DESC", (roll_no,))
        return jsonify({'status': 'success', 'data': cursor.fetchall()})
    finally:
        cursor.close()
        conn.close()

@student_bp.route('/timetable', methods=['GET'])
@student_required
def get_timetable():
    roll_no = session.get('roll_no')
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT branch, year, section FROM students WHERE roll_no = ?", (roll_no,))
        s = cursor.fetchone()
        cursor.execute("""
            SELECT t.day, t.period, s.name as subject, tch.name as teacher
            FROM timetable t
            JOIN subjects s ON t.subject_id = s.id
            JOIN teachers tch ON t.teacher_id = tch.teacher_id
            WHERE t.branch = ? AND t.year = ? AND t.section = ?
            ORDER BY CASE day 
                WHEN 'Monday' THEN 1 WHEN 'Tuesday' THEN 2 WHEN 'Wednesday' THEN 3 
                WHEN 'Thursday' THEN 4 WHEN 'Friday' THEN 5 END, period
        """, (s['branch'], s['year'], s['section']))
        return jsonify({'status': 'success', 'data': cursor.fetchall()})
    finally:
        cursor.close()
        conn.close()

@student_bp.route('/calendar', methods=['GET'])
def get_calendar():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM academic_calendar ORDER BY start_date")
        cal = cursor.fetchall()
        cursor.execute("SELECT * FROM holidays ORDER BY date")
        hols = cursor.fetchall()
        return jsonify({'status': 'success', 'data': {'calendar': cal, 'holidays': hols}})
    finally:
        cursor.close()
        conn.close()

