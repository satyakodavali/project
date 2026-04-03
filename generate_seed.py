import random
import os
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

random.seed(42)

NUM_STUDENTS = 1000
STUDENT_PASSWORD = "Pass123!" 
ADMIN_PASSWORD = "Admin12!"

BRANCHES = ['CSE', 'ECE', 'CIVIL', 'MECH', 'EEE', 'IT']
SECTIONS = ['A', 'B', 'C']
RELIGIONS = ['Hindu', 'Muslim', 'Christian', 'Sikh']
GENDERS = ['Male', 'Female']

REAL_FACULTY = [
    "Ms. KILAPARTHY PUNYAVATHI PUSHPA",
    "MARRI BHARGAVI",
    "M L SOWJANYA",
    "M.S.S.VAHINI",
    "Mr. E. SIVA KRUSHNA",
    "Mr. D. APPALARAJU",
    "Mr. ATCHUT VARDHAN KALAVALA",
    "Mrs. PALIKI PADMA",
    "Prof. Alekhya Rao",
    "Prof. Santosh Varma",
    "Prof. Sowmya Naidu",
    "Prof. Ramesh Kumar",
    "Prof. Haritha Rao",
    "Prof. Prasad Reddy",
    "Prof. Gayathri Chowdary",
    "Prof. Rakesh Patel"
]

male_first_names = ["Rahul", "Ravi", "Suresh", "Ramesh", "Venkata", "Sai", "Anil", "Kumar", "Akhil", "Arjun", "Karthik", "Raja", "Hari", "Prasad", "Naveen"]
female_first_names = ["Lakshmi", "Priya", "Gayathri", "Sanjana", "Neha", "Divya", "Swathi", "Sowmya", "Anusha", "Manasa", "Pooja", "Kavya", "Revathi"]
last_names = ["Reddy", "Rao", "Naidu", "Chowdary", "Varma", "Sharma", "Yadav", "Goud", "Mishra", "Patel", "Kumar", "Das", "Gupta", "Singh"]

def generate_student(i, hashed_pw):
    year_prefixes = [21, 22, 23, 24]
    year_prefix = year_prefixes[i % 4]
    year = 2025 - (2000 + year_prefix)
    branch = BRANCHES[(i // 4) % len(BRANCHES)]
    section = SECTIONS[(i // 24) % len(SECTIONS)]
    roll_no = f"{year_prefix}{branch}{100+i:03d}"
    
    # Priority for 24CSE100 which the user uses
    if i == 0:
        roll_no = "24CSE100"; year=1; branch="CSE"; section="A"; name="Akhil Das"; gender="Male"
    else:
        gender = GENDERS[i % 2]
        first = male_first_names[i % len(male_first_names)] if gender == "Male" else female_first_names[i % len(female_first_names)]
        name = f"{first} {last_names[i % len(last_names)]}"

    adm_no = f"ADM{roll_no}"
    dob = (datetime(2005, 1, 1) + timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')
    rel = random.choice(RELIGIONS)
    phone = f"9848{random.randint(100000, 999999)}"
    # User requested to use only these 4 working test numbers
    test_mobile_numbers = ["9398344060", "9182995461", "9542138529", "9391549259"]
    parents_mobile = random.choice(test_mobile_numbers)
    em = f"{roll_no.lower()}@nsrit.edu.in"
    aa = f"{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
    addr = f"H.No {random.randint(1, 500)}, Street {random.randint(1, 20)}, Visakhapatnam, AP"
    f_name = f"{random.choice(male_first_names)} {random.choice(last_names)}"
    m_name = f"{random.choice(female_first_names)} {random.choice(last_names)}"
    occ = random.choice(["Engineer", "Doctor", "Teacher", "Farmer", "Business"])
    join = "2024-07-15" if year == 1 else "2023-07-15"
    inc = random.randint(150000, 1000000)
    hostel = 1 if i % 5 == 0 else 0
    current_sem = f"{year}-1" if i % 2 == 0 else f"{year}-2"

    cols = "(roll_no, admission_no, name, branch, section, year, gender, dob, religion, phone, email, aadhar, address, father_name, mother_name, parents_occupation, parents_mobile, annual_income, joining_date, photo_url, is_hosteller, password_hash, current_semester)"
    vals = f"('{roll_no}', '{adm_no}', '{name}', '{branch}', '{section}', {year}, '{gender}', '{dob}', '{rel}', '{phone}', '{em}', '{aa}', '{addr}', '{f_name}', '{m_name}', '{occ}', '{parents_mobile}', {inc}, '{join}', '', {hostel}, '{hashed_pw}', '{current_sem}')"
    return f"INSERT INTO students {cols} VALUES {vals};\n", roll_no, year, branch, section, hostel, current_sem

def run():
    hashed_student = generate_password_hash(STUDENT_PASSWORD)
    hashed_admin = generate_password_hash(ADMIN_PASSWORD)
    seed_path = os.path.join(os.path.dirname(__file__), "seed_data.sql")
    
    with open(seed_path, "w", encoding='utf-8') as f:
        f.write("-- NSRIT Professional Seed Data\n\n")
        f.write(f"INSERT INTO admins (username, password_hash) VALUES ('admin', '{hashed_admin}');\n\n")
        
        teacher_ids = []
        for i, name in enumerate(REAL_FACULTY):
            tid = f"TCH{i+1:03d}"
            dept = BRANCHES[i % len(BRANCHES)]
            f.write(f"INSERT INTO teachers (teacher_id, name, department) VALUES ('{tid}', '{name}', '{dept}');\n")
            teacher_ids.append(tid)
        
        for b in BRANCHES:
            for y in [1, 2, 3, 4]:
                for s in SECTIONS:
                    f.write(f"INSERT INTO class_teachers (teacher_id, branch, year, section) VALUES ('{random.choice(teacher_ids)}', '{b}', {y}, '{s}');\n")

        subject_ids = {}
        base_curriculum = [
            ('1-1', [('101', 'Programming in C', 3), ('102', 'Maths I', 4), ('103', 'Physics', 3), ('104', 'English Lab', 1.5), ('105', 'Physics Lab', 1.5)]),
            ('1-2', [('201', 'Data Structures', 3), ('202', 'Electrical Basics', 3), ('203', 'Maths II', 3), ('204', 'DS Lab', 1.5), ('205', 'Basic Eng', 3)]),
            ('2-1', [('301', 'Core Subject 1', 3), ('302', 'Database Sys', 3), ('303', 'Operating Sys', 3), ('304', 'Core Lab I', 1.5), ('305', 'Aptitude', 2)]),
            ('2-2', [('401', 'Core Subject 2', 3), ('402', 'Analysis', 3), ('403', 'Software Eng', 3), ('404', 'Core Lab II', 1.5), ('405', 'Seminar I', 1)]),
            ('3-1', [('501', 'Advanced Core 1', 3), ('502', 'Networks', 3), ('503', 'Design', 3), ('504', 'Network Lab', 1.5), ('505', 'Mini Project', 2)]),
            ('3-2', [('601', 'Cloud tech', 3), ('602', 'Machine Learning', 3), ('603', 'Modern Tools', 3), ('604', 'Tools Lab', 1.5), ('605', 'Internship Eval', 2)]),
            ('4-1', [('701', 'Cyber Security', 3), ('702', 'Elective I', 3), ('703', 'Elective II', 3), ('704', 'Project Phase I', 3)]),
            ('4-2', [('801', 'Project Phase II', 9), ('802', 'Technical Seminar', 3)])
        ]
        
        extra_names = ['SPM', 'STM', 'PE', 'FS', 'SEM', 'RC', 'MEN', 'OE4', 'OE2', 'CSP', 'FSI', 'CP', 'DI', 'NPTEL', 'TT']
        sid_counter = 1
        for b in BRANCHES:
            subject_ids[b] = {}
            for sem, subs in base_curriculum:
                subject_ids[b][sem] = []
                ext_subs = list(subs)
                sem_limit = 8 # Always 8 subjects to match 8 periods
                while len(ext_subs) < sem_limit:
                    idx = len(ext_subs); name = extra_names[idx % len(extra_names)]; ext_subs.append((f"X-{sem}-{idx}", name, 0))
                for code, name, cred in ext_subs:
                    scode = f"{b}{code}"; sname = f"{name} ({b})" if not code.startswith('X') else name
                    f.write(f"INSERT INTO subjects (subject_code, name, branch, semester, credits) VALUES ('{scode}', '{sname}', '{b}', '{sem}', {cred});\n")
                    subject_ids[b][sem].append((sid_counter, sname, cred))
                    sid_counter += 1

        for i in range(NUM_STUDENTS):
            stmt, roll, year, branch, section, is_hostel, current_sem = generate_student(i, hashed_student)
            f.write(stmt)
            f.write(f"INSERT INTO mentors (student_roll_no, teacher_id) VALUES ('{roll}', '{random.choice(teacher_ids)}');\n")
            sems_list = ['1-1', '1-2', '2-1', '2-2', '3-1', '3-2', '4-1', '4-2']
            num_completed = 1 if roll == "24CSE100" else (year - 1) * 2
            completed_sems = sems_list[:num_completed]
            cum_gp_cred = 0; cum_cred = 0
            for sem in completed_sems:
                s_gp_c = 0; s_c = 0
                for sid, name, cred in subject_ids[branch][sem]:
                    grade = random.choice(['O', 'A+', 'A', 'B+', 'B']); gp = {'O':10, 'A+':9, 'A':8, 'B+':7, 'B':6}[grade]
                    f.write(f"INSERT INTO marks (student_roll_no, subject_id, grade, grade_point, credits) VALUES ('{roll}', {sid}, '{grade}', {gp}, {cred});\n")
                    if cred > 0: s_gp_c += gp * cred; s_c += cred
                    held = random.randint(60, 90); att = int(held * random.uniform(0.65, 0.98))
                    f.write(f"INSERT INTO attendance (student_roll_no, subject_id, classes_held, classes_attended) VALUES ('{roll}', {sid}, {held}, {att});\n")
                    f.write(f"INSERT INTO internal_marks (student_roll_no, subject_id, mid1, mid2, assignments, online_tests, lab_marks) VALUES ('{roll}', {sid}, {random.randint(15,25)}, {random.randint(15,25)}, 10, 10, 25);\n")
                sgpa = round(s_gp_c / s_c, 2) if s_c > 0 else 0; cum_gp_cred += s_gp_c; cum_cred += s_c
                cgpa = round(cum_gp_cred / cum_cred, 2) if cum_cred > 0 else 0
                f.write(f"INSERT INTO semester_results (student_roll_no, semester, sgpa, cgpa, total_credits, percentage) VALUES ('{roll}', '{sem}', {sgpa}, {cgpa}, {s_c}, {sgpa*10});\n")
            for sid, name, cred in subject_ids[branch][current_sem]:
                held = random.randint(40, 80); att = random.randint(20, held)
                f.write(f"INSERT INTO attendance (student_roll_no, subject_id, classes_held, classes_attended) VALUES ('{roll}', {sid}, {held}, {att});\n")
                f.write(f"INSERT INTO internal_marks (student_roll_no, subject_id, mid1, mid2, assignments, online_tests, lab_marks) VALUES ('{roll}', {sid}, {random.randint(12,25)}, {random.randint(12,25)}, 5, 5, 25);\n")
            final_cg = round(cum_gp_cred/cum_cred, 2) if cum_cred > 0 else 0.0
            f.write(f"INSERT INTO cgpa (student_roll_no, cgpa, total_credits, total_percentage) VALUES ('{roll}', {final_cg}, {cum_cred}, {final_cg*10});\n")
            f.write(f"INSERT INTO fees (student_roll_no, academic_year, tuition_fees, convener_fees, management_fees, hostel_fees, paid_fees, due_date) VALUES ('{roll}', '2024-25', 50000, 15000, 0, {50000 if is_hostel else 0}, 30000, '2025-06-30');\n")
            if is_hostel:
                f.write(f"INSERT INTO hostel_records (student_roll_no, room_no, hostel_fees) VALUES ('{roll}', 'A-{100+i}', 50000);\n")
                f.write(f"INSERT INTO outing_records (roll_number, date, out_time, in_time, reason) VALUES ('{roll}', '2025-03-01', '09:00', '18:00', 'Home visit');\n")

        calendar_events = [('2025-04-10', '2025-04-12', 'MID-I Exams - Sem I', 'Exam'), ('2025-05-15', '2025-05-18', 'MID-II Exams - Sem I', 'Exam'), ('2025-06-10', '2025-06-25', 'Semester End Exams - Sem I', 'Exam')]
        for start, end, desc, etype in calendar_events:
            f.write(f"INSERT INTO academic_calendar (start_date, end_date, description, event_type) VALUES ('{start}', '{end}', '{desc}', '{etype}');\n")
        
        for b in BRANCHES:
            for y in [1, 2, 3, 4]:
                for s in SECTIONS:
                    for sem_suffix in ['-1', '-2']:
                        current_sem = f"{y}{sem_suffix}"
                        subs = subject_ids[b][current_sem]
                        # Use at most len(REAL_FACULTY) unique teachers per section
                        section_teachers = random.sample(teacher_ids, min(len(subs), len(teacher_ids)))
                        sub_teacher_map = {subs[j][0]: section_teachers[j % len(section_teachers)] for j in range(len(subs))}
                        
                        for d in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
                            day_subs = random.sample(subs, 8)
                            for p in range(1, 9):
                                sid, name, cred = day_subs[p-1]
                                tid = sub_teacher_map[sid]
                                f.write(f"INSERT INTO timetable (branch, year, section, day, period, subject_id, teacher_id) VALUES ('{b}', {y}, '{s}', '{d}', {p}, {sid}, '{tid}');\n")

if __name__ == "__main__":
    run()

