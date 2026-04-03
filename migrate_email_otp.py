import sqlite3
import os
import random

def migrate_and_seed():
    db_path = r'c:\Users\LENOVO\NewCollegeChatBot\college-portal\backend\nsrit_portal.db'
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # 1. Add parents_email column if it doesn't exist
        cursor.execute("PRAGMA table_info(students)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'parents_email' not in columns:
            print("Adding 'parents_email' column to 'students' table...")
            cursor.execute("ALTER TABLE students ADD COLUMN parents_email VARCHAR(100)")
            conn.commit()
        else:
            print("'parents_email' column already exists.")

        # 2. Seed provided Gmail IDs
        emails = [
            "navadeepreyyi1419@gmail.com",
            "rahulkumarporida7788@gmail.com",
            "nandinipriyatangeti10@gmail.com",
            "sanjupedaprolu@gmail.com"
        ]

        cursor.execute("SELECT roll_no FROM students")
        students = cursor.fetchall()
        
        if not students:
            print("No students found in the database to seed.")
            return

        print(f"Seeding {len(students)} students with Gmail IDs...")
        for student in students:
            email = random.choice(emails)
            cursor.execute("UPDATE students SET parents_email = ? WHERE roll_no = ?", (email, student[0]))
        
        conn.commit()
        print("Seeding completed successfully.")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_and_seed()
