-- NSRIT College Portal Database Schema (Architectural Compliance)

CREATE TABLE admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL, -- Hashed passwords
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE teachers (
    teacher_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(50) NOT NULL
);

CREATE TABLE class_teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id VARCHAR(20) NOT NULL,
    branch VARCHAR(50) NOT NULL,
    year INTEGER NOT NULL,
    section VARCHAR(10) NOT NULL,
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id) ON DELETE CASCADE
);

CREATE TABLE students (
    roll_no VARCHAR(20) PRIMARY KEY,
    admission_no VARCHAR(20) UNIQUE,
    name VARCHAR(100) NOT NULL,
    course VARCHAR(50) DEFAULT 'B.Tech',
    branch VARCHAR(50) NOT NULL,
    year INTEGER NOT NULL,
    section VARCHAR(10) NOT NULL,
    gender VARCHAR(10),
    dob DATE,
    nationality VARCHAR(50) DEFAULT 'Indian',
    religion VARCHAR(50),
    phone VARCHAR(15),
    email VARCHAR(100),
    aadhar VARCHAR(20),
    address TEXT,
    father_name VARCHAR(100),
    mother_name VARCHAR(100),
    parents_occupation VARCHAR(100),
    parents_mobile VARCHAR(15),
    annual_income DECIMAL(12,2),
    joining_date DATE,
    photo_url TEXT,
    is_hosteller BOOLEAN DEFAULT 0,
    password_hash TEXT NOT NULL, -- Hashed passwords
    current_semester VARCHAR(10) DEFAULT '1-1',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE mentors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_roll_no VARCHAR(20) NOT NULL,
    teacher_id VARCHAR(20) NOT NULL,
    FOREIGN KEY (student_roll_no) REFERENCES students(roll_no) ON DELETE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id) ON DELETE CASCADE
);

CREATE TABLE subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    branch VARCHAR(50) NOT NULL,
    semester VARCHAR(10) NOT NULL, -- e.g., '1-1', '1-2'
    credits INTEGER NOT NULL
);

-- Aggregated Attendance
CREATE TABLE attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_roll_no VARCHAR(20) NOT NULL,
    subject_id INTEGER NOT NULL,
    classes_held INTEGER DEFAULT 0,
    classes_attended INTEGER DEFAULT 0,
    FOREIGN KEY (student_roll_no) REFERENCES students(roll_no) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
);

-- Day-to-Day Attendance (Academic Register)
CREATE TABLE daily_attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_number VARCHAR(20) NOT NULL,
    date DATE NOT NULL,
    subject VARCHAR(100) NOT NULL,
    classes_held INTEGER DEFAULT 1,
    present_or_absent VARCHAR(10) CHECK(present_or_absent IN ('Present', 'Absent')) NOT NULL,
    FOREIGN KEY (roll_number) REFERENCES students(roll_no) ON DELETE CASCADE
);

CREATE TABLE semester_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_roll_no VARCHAR(20) NOT NULL,
    semester VARCHAR(10) NOT NULL,
    sgpa DECIMAL(4,2) NOT NULL,
    cgpa DECIMAL(4,2) NOT NULL, -- Added to track historical CGPA
    total_credits INTEGER DEFAULT 0,
    percentage DECIMAL(5,2) DEFAULT 0.00,
    FOREIGN KEY (student_roll_no) REFERENCES students(roll_no) ON DELETE CASCADE,
    UNIQUE(student_roll_no, semester)
);

-- Link subjects to marks for semester results detail
CREATE TABLE marks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_roll_no VARCHAR(20) NOT NULL,
    subject_id INTEGER NOT NULL,
    grade VARCHAR(2) NOT NULL,
    grade_point INTEGER NOT NULL,
    credits INTEGER NOT NULL,
    FOREIGN KEY (student_roll_no) REFERENCES students(roll_no) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
);

CREATE TABLE cgpa (
    student_roll_no VARCHAR(20) PRIMARY KEY,
    cgpa DECIMAL(4,2) NOT NULL,
    total_credits INTEGER DEFAULT 0,
    total_percentage DECIMAL(5,2) DEFAULT 0.00,
    FOREIGN KEY (student_roll_no) REFERENCES students(roll_no) ON DELETE CASCADE
);

CREATE TABLE internal_marks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_roll_no VARCHAR(20) NOT NULL,
    subject_id INTEGER NOT NULL,
    mid1 INTEGER DEFAULT 0,
    mid2 INTEGER DEFAULT 0,
    assignments INTEGER DEFAULT 0,
    online_tests INTEGER DEFAULT 0,
    lab_marks INTEGER DEFAULT 0,
    FOREIGN KEY (student_roll_no) REFERENCES students(roll_no) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
);

CREATE TABLE backlogs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_roll_no VARCHAR(20) NOT NULL,
    subject_id INTEGER NOT NULL,
    semester VARCHAR(10) NOT NULL,
    FOREIGN KEY (student_roll_no) REFERENCES students(roll_no) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
);

CREATE TABLE fees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_roll_no VARCHAR(20) NOT NULL,
    academic_year VARCHAR(20) NOT NULL,
    tuition_fees DECIMAL(10,2) DEFAULT 0.00,
    convener_fees DECIMAL(10,2) DEFAULT 0.00,
    management_fees DECIMAL(10,2) DEFAULT 0.00,
    hostel_fees DECIMAL(10,2) DEFAULT 0.00,
    paid_fees DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    due_date DATE NOT NULL,
    FOREIGN KEY (student_roll_no) REFERENCES students(roll_no) ON DELETE CASCADE
);

CREATE TABLE hostel_records (
    student_roll_no VARCHAR(20) PRIMARY KEY,
    room_no VARCHAR(10),
    hostel_fees DECIMAL(10,2),
    is_active BOOLEAN DEFAULT 1,
    FOREIGN KEY (student_roll_no) REFERENCES students(roll_no) ON DELETE CASCADE
);

CREATE TABLE outing_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_number VARCHAR(20) NOT NULL,
    date DATE NOT NULL,
    out_time TIME,
    in_time TIME,
    reason TEXT,
    FOREIGN KEY (roll_number) REFERENCES students(roll_no) ON DELETE CASCADE
);

CREATE TABLE academic_calendar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    start_date DATE NOT NULL,
    end_date DATE,
    description VARCHAR(255) NOT NULL,
    event_type VARCHAR(50) -- Holiday, Fest, Exam
);

CREATE TABLE holidays (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    description VARCHAR(255) NOT NULL
);

CREATE TABLE timetable (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    branch VARCHAR(50) NOT NULL,
    year INTEGER NOT NULL,
    section VARCHAR(10) NOT NULL,
    day VARCHAR(20) NOT NULL,
    period INTEGER NOT NULL,
    subject_id INTEGER,
    teacher_id VARCHAR(20),
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE SET NULL,
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id) ON DELETE SET NULL
);

