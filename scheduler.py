import datetime
from utils.db import get_db_connection

def get_holidays():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT date FROM holidays")
    holidays = {row['date'] for row in cursor.fetchall()}
    
    cursor.execute("SELECT start_date FROM academic_calendar WHERE event_type IN ('Holiday', 'Fest')")
    fests = {row['start_date'] for row in cursor.fetchall()}
    
    conn.close()
    return holidays.union(fests)

def generate_mid_timetable(start_date_str, subjects_list):
    # Continuous, max 5 days, skip Sunday/holiday
    holidays = get_holidays()
    curr_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
    timetable = []
    
    for sub in subjects_list[:5]: # Max 5 days
        while True:
            # Skip Sunday (6 is Sunday in weekday() if Monday is 0)
            # Wait, weekday() 0 is Mon, 6 is Sun.
            if curr_date.weekday() == 6 or curr_date.strftime('%Y-%m-%d') in holidays:
                curr_date += datetime.timedelta(days=1)
                continue
            break
        
        timetable.append({"date": curr_date.strftime('%Y-%m-%d'), "subject": sub})
        curr_date += datetime.timedelta(days=1)
        
    return timetable

def generate_sem_timetable(start_date_str, subjects_list):
    # Alternate days, skip Sunday/holiday/festival
    holidays = get_holidays()
    curr_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
    timetable = []
    
    for sub in subjects_list:
        while True:
            if curr_date.weekday() == 6 or curr_date.strftime('%Y-%m-%d') in holidays:
                curr_date += datetime.timedelta(days=1)
                continue
            break
        
        timetable.append({"date": curr_date.strftime('%Y-%m-%d'), "subject": sub})
        # Preparation holiday (skip next day)
        curr_date += datetime.timedelta(days=2)
        
    return timetable

def get_backlog_exam_schedule(subject_name, semester):
    # Identify next available exam date for this subject
    # Logic: Look for the earliest exam date in academic_calendar that matches sem
    # For now, let's mock it or find it from generated timetables.
    # We'll just provide a placeholder date based on the semester end exam.
    conn = get_db_connection()
    cursor = conn.cursor()
    # Find Sem End Exam for the semester type (Odd/Even)
    is_odd = any(s in semester for s in ['1', '3', '5', '7'])
    desc = "Semester End Exams - Sem I" if is_odd else "Semester End Exams - Sem II"
    
    cursor.execute("SELECT start_date FROM academic_calendar WHERE description LIKE ?", (f"%{desc}%",))
    row = cursor.fetchone()
    conn.close()
    
    date = row['start_date'] if row else "TBD"
    return f"Your backlog exam for {subject_name} is scheduled on {date}. Prepare well."
